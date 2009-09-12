
from django.core.management.base import NoArgsCommand
from djangopeople import clustering

class Command(NoArgsCommand):
    
    help = "Re-runs the server-side clustering"

    def handle_noargs(self, **options):
        clustering.run()