
def distance(float x1, float y1, float x2, float y2):
    "Pythagorean distance"
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def closest_pair(list points):
    """
    Returns the closest pair of points as (distance, (x, y, data), (x2, y2, data2)).
    
    @param points: A list of triples (x, y, data)
    """
    
    cdef float min_d
    
    if len(points) < 2:
        raise ValueError("Single or empty points set")
    elif 2 <= len(points) <= 6: # 6 seems about the sweet spot
        min_d = 0
        min_p1 = None
        min_p2 = None
        for i, point in enumerate(points):
            for point2 in points[i+1:]:
                d = distance(point[0], point[1], point2[0], point2[1])
                if min_d == 0 or min_d > d:
                    min_d = d
                    min_p1 = point
                    min_p2 = point2
        return min_d, min_p1, min_p2
    else:
        points.sort()
        # Split into two subproblems
        split = int(len(points) / 2)
        d1, p11, p12 = closest_pair(points[:split])
        d2, p21, p22 = closest_pair(points[split:])
        d = min(d1, d2)
        # Merge (see: http://web.archive.org/web/20080207223230/http://www.cs.mcgill.ca/~cs251/ClosestPair/ClosestPairDQ.html)
        points_in_strip = []
        split_at = (points[split-1][0] + points[split][0]) / 2.0
        for point in points:
            if point[0] < (split_at-d):
                continue
            elif point[0] > (split_at+d):
                break
            points_in_strip.append((point[1], point[0], point[2]))
        # Sort by y
        points_in_strip.sort()
        # Now check all points in strip
        min_d = 0
        min_p1 = None
        min_p2 = None
        max_i = len(points_in_strip)
        for (i, point) in enumerate(points_in_strip):
            for point2 in points_in_strip[i+1:min(max_i, i+7)]:
                sd = distance(point[0], point[1], point2[0], point2[1])
                if min_d == 0 or min_d > sd:
                    min_d = sd
                    min_p1 = (point[1], point[0], point[2])
                    min_p2 = (point2[1], point2[0], point2[2])
        if min_d != 0 and min_d < d:
            return min_d, min_p1, min_p2
        elif d1 < d2:
            return d1, p11, p12
        else:
            return d2, p21, p22
    
    