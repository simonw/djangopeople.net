
import sys
import time
from clusterlizard.closestpair import closest_pair

# Some simple functions

def mean(l):
    return sum(l)/float(len(l))

# Cluster class

class Cluster(object):
    
    def __init__(self, iterable):
        self.points = set(iterable)
        self.mean = self._mean()
    
    def _mean(self):
        xs, ys = [], []
        for x, y, d in self.points:
            xs.append(x)
            ys.append(y)
        return mean(xs), mean(ys)
    
    def merge(self, other):
        return Cluster(self.points.union(other.points))
    
    def distance(self, other):
        return distance(self.mean, other.mean)
    
    def __len__(self):
        return len(self.points)


class Clusterer(object):
    
    def __init__(self, input, output, progress=None, separation=75):
        self.input = input
        self.output = output
        self.progress = progress
        self.separation = separation
    
    def run(self):
        "Runs the cluster analysis."
        
        clusters = set(Cluster([(x, y, d)]) for x, y, d in self.input)
        
        d = 0
        i = 0
        zoom = 17
        tooks = []
        
        while zoom >= 0:
            # Work out what separation is at this zoom
            m_per_pixel = (40075016.68 / 2**zoom) / 256
            max_sep = m_per_pixel * self.separation
            # Keep going until clusters are far apart or not very numerous.
            
            while d < max_sep and len(clusters) > 1:
                s = time.time()
                # Use closest-pair to find the closest two clusters
                d, (x1, y1, c1), (x2, y2, c2) = closest_pair([(c.mean[0], c.mean[1], c) for c in clusters])
                if d >= max_sep:
                    break
                # Merge them in the set
                cn = c1.merge(c2)
                clusters.discard(c1)
                clusters.discard(c2)
                clusters.add(cn)
                # Calculate stats
                i += 1
                tooks = [time.time() - s] + tooks[:2]
                took = mean(tooks)
                eta = took * (len(clusters) - 10) * 0.7
                eta = "%i:%i" % (eta/60, eta%60)
                if self.progress:
                    self.progress(i, len(clusters)-1, took, zoom, eta)
            self.output(clusters, zoom)
            zoom -= 1
