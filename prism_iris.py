from turtle import *
from colorsys import *

# popup window
setup(800,725)
speed(0.6)
tracer(20)
bgcolor("black")


h = 10
for i in range(360):
    c = hsv_to_rgb(h,1,1)
    color (c)
    h += 0.005
    circle(150)
    circle (10)
    circle(30)
    circle(60)
    left(2)
    dot(20)
    left(10)
done()