
from clusterlizard.clusterer import Clusterer

from djangopeople.models import *

def input_generator():
    """
    The input to ClusterLizard should be a generator that yields (mx,my,id) tuples.
    This function reads them from the DjangoPeople models.
    """
    for person in DjangoPerson.objects.all():
        yield (person.longitude, person.latitude, person.id)
    
    
def save_clusters(clusters, zoom):
    """
    The output function provided to ClusterLizard should be a
    function that takes 'clusters', a set of clusters, and 'zoom',
    the integer Google zoom level.
    """
    for cluster in clusters:
        ClusteredPoint.objects.create(
            latitude = cluster.mean[0],
            longitude = cluster.mean[1],
            number = len(cluster),
            zoom = zoom,
        )


def progress(done, left, took, zoom, eta):
    """
    You can also pass in an optional progress callback.
    """
    print "Iter %s (%s clusters) [%.3f secs] [zoom: %s] [ETA %s]" % (done, left, took, zoom, eta)


def run():
    """
    Runs the clustering, clearing the DB first.
    """
    ClusteredPoint.objects.all().delete()
    clusterer = Clusterer(
        input_generator(),
        save_clusters,
        progress,
    )
    clusterer.run()