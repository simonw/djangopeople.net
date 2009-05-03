from django import template

register = template.Library()

@register.inclusion_tag('_person_list_items.html')
def person_list_items(people):
    return {'people': people}
