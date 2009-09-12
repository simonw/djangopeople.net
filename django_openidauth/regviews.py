from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

try:
    # dependency: http://code.google.com/p/django-registration
    from registration.forms import RegistrationForm
    from registration.models import RegistrationProfile
except ImportError, e:
    raise ImportError, (
        "Could not import a required dependency: please ensure that " +
        "django-registration is installed and available on the Python Path " +
        "as 'registration'. Try 'import registration' at a Python prompt to " +
        "confirm installation. django-registration is available from " +
        "http://code.google.com/p/django-registration\n\n%s" % str(e)
    )

class RegistrationFormOpenID(RegistrationForm):
    """
    This form requires access to the Django request object in order to properly
    validate itself, as the password field is only required if an OpenID is not
    currently available as part of the request. The request object can be 
    passed to the constructor as a named keyword argument called 'request'
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request', None)
        if 'request' in kwargs:
            del kwargs['request']
        super(RegistrationFormOpenID, self).__init__(*args, **kwargs)
        self.base_fields['password1'].required = False
        self.base_fields['password2'].required = False
    
    def clean_password1(self):
        "Password is only required if user is not registering with an OpenID"
        if not self.request or not getattr(self.request, 'openids', []):
            # No OpenID, so password field is required
            if 'password1' not in self.cleaned_data \
                or not self.cleaned_data.get('password1', '').strip():
                raise forms.ValidationError(u'You must provide a password')
        return self.cleaned_data.get('password1', '')

def register(request, success_url='/accounts/register/complete/', 
        template_name='registration_form.html'):
    """
    Allows a new user to register an account. A customised variation of the 
    view of the same name from django-registration.

    Context::
        form
            The registration form
    
    Template::
        registration/registration_form.html (or template_name argument)
    
    """
    if request.method == 'POST':
        form = RegistrationFormOpenID(request.POST, request=request)
        if form.is_valid():
            new_user = RegistrationProfile.objects.create_inactive_user(username=form.cleaned_data['username'],
                                                                        password=form.cleaned_data['password1'],
                                                                        email=form.cleaned_data['email'])
            return HttpResponseRedirect(success_url)
    else:
        form = RegistrationForm()
    return render_to_response(template_name, { 'form': form },
                              context_instance=RequestContext(request))

def demo_delete_me_asap(request):
    import django.forms
    
    class UserProfileForm(forms.Form):
        name = forms.CharField(max_length=100)
        email = forms.EmailField()
        bio = forms.CharField(widget=forms.Textarea)
        dob = forms.DateField(required=False)
        receive_newsletter = forms.BooleanField(required=False)
        def clean_email(self):
            from django.forms.util import ValidationError
            if self.cleaned_data['email'].split('@')[1] == 'hotmail.com':
                raise ValidationError, "No hotmail.com emails, please."

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # ... save the user's profile
            return HttpResponseRedirect('/profile/saved/')
    else:
        form = UserProfileForm()
    return render_to_response('profile.html', {'form': form})
