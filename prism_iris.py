import turtle as t
from colorsys import hsv_to_rgb

# popup window
t.setup(800, 725)
t.tracer(20)
t.bgcolor("black")


h = 0
for i in range(360):
    c = hsv_to_rgb(h, 1, 1)
    t.color(c)
    h += 0.005
    t.circle(150)
    t.circle(10)
    t.circle(30)
    t.circle(60)
    t.left(2)
    t.dot(20)
    t.left(10)
t.done()
