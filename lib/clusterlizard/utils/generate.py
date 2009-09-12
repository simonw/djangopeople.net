
import random
import math


def latlong_to_mercator(lat, long):
    x = long * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34 / 180;
    return x, y


def mercator_to_latlong(x, y):
    long = (x / 20037508.34) * 180
    lat = (y / 20037508.34) * 180
    lat = 180/math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return lat, long



def random():
    f = open("points.csv", "w")
    
    for i in range(500):
        x = random.uniform(-20037508.34, 20037508.34)
        y = random.uniform(-15037508.34, 15037508.34)
        f.write('%s,%s,"Point %i"\n' % (x, y, i))
    
    f.close()

    
def geonames(file):
    f = open("cities.csv", "w")
    
    for row in file:
        items = row.split("\t")
        lat = float(items[4])
        long = float(items[5])
        name = items[1]
        x, y = latlong_to_mercator(lat, long)
        f.write('%s,%s,"%s"\n' % (x, y, name))
    
    f.close()

geonames(open("cities15000.txt"))
    
    