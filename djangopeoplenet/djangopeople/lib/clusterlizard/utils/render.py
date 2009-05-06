
import cairo
import sys
import os
import math

width, height = 600.0, 600.0
mx1, my1, mx2, my2 = [-20037508.34, 20037508.34, 20037508.34, -20037508.34]
mxr = mx2 - mx1
myr = my2 - my1

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
context = cairo.Context(surface)

def m_to_px(x, y):
    return ((x-mx1)/mxr)*width, ((y-my1)/myr)*height

context.set_source_rgba(1,1,1,1)
context.paint()
    
for row in open(sys.argv[1]):
    x, y, label = row.split(",")
    px, py = m_to_px(float(x), float(y))
    try:
        r = int(label)/100 + 1
    except ValueError:
        r = 2
    context.arc(px, py, r, 0, math.pi*2)
    context.set_source_rgba(0,0.2,0.6,0.8)
    context.fill()

surface.write_to_png("output.png")
surface.finish()

os.system("display output.png")