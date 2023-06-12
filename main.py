import ctypes
import platform
import pyglet
from time import time
import math
import multiprocessing as mp


# set process DPI aware
def set_process_dpi_aware():
    system = platform.uname()
    if system.system == 'Windows' and float(system.release) > 6:
        ctypes.windll.user32.SetProcessDPIAware()
set_process_dpi_aware()

# basic setup
RE_START = -2
RE_END = 2
IM_START = -1
IM_END = 1
WIDTH = 900
HEIGHT = math.ceil((IM_END-IM_START)*WIDTH/(RE_END-RE_START))

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
batch = pyglet.graphics.Batch()

color = color=(23, 124, 98)
backgournd = pyglet.shapes.Rectangle(0, 0, WIDTH, HEIGHT, color=(255, 255, 255), batch=batch)

## ejes
eje_y = pyglet.shapes.Rectangle(WIDTH/2, 0, 1, HEIGHT, color=(0, 0, 0), batch=batch)
eje_x = pyglet.shapes.Rectangle(0, HEIGHT/2, WIDTH, 1, color=(0, 0, 0), batch=batch)

MAX_ITER = 80

#Now we are trying to parallelize

# Here the idea is to recibe point to use in lambda, when generating (Px, Py) a tuple
def mandelbrot(point):
    """ Determines if the point is in the mandelbrot set or not"""
    Px, Py = point
    x0 = Px/WIDTH*(RE_END - RE_START) + RE_START
    y0 = Py/HEIGHT*(IM_END - IM_START) + IM_START
    iteration = 0
    c = complex(x0, y0)
    z = complex(0,0)
    while abs(z) < 2 and iteration <= MAX_ITER:
        z = z*z +c
        iteration += 1

    return abs(z) <= 2



# Plot window

# just the point in the mandelbrot set
points = filter(mandelbrot, ((Px,Py) for Py in range(HEIGHT) for Px in range(WIDTH)))
# create the 'pixels' for those points
pixels = map(lambda p:  pyglet.shapes.Rectangle(p[0], p[1], 1, 1, color=(0, 0, 0), batch=batch), points)
current_time = time()
screen = list(pixels) # this is what cost time
print(time()-current_time)
workers = mp.cpu_count()

print(workers)
# We cannot use multiprocessing because we cannot share openGL context, so the following won't work

# with mp.Pool(workers-1) as P:
#     screen = P.map(lambda p:  pyglet.shapes.Rectangle(p[0], p[1], 1, 1, color=(0, 0, 0), batch=batch), points)



@window.event
def on_draw():
    window.clear()
    batch.draw()

if __name__ == '__main__':
    pyglet.app.run()

