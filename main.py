import ctypes
import platform
import pyglet
from time import time
import math
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
plane = [[None] * HEIGHT for _ in range(WIDTH)]

MAX_ITER = 80
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z=z*z +c
        n += 1
    return n

# Plot window

esta = []
def mandelbrot_set(plane):
    for Px in range(WIDTH):
        for Py in range(HEIGHT):
            x0 = Px/WIDTH*(RE_END - RE_START) + RE_START
            y0 = Py/HEIGHT*(IM_END - IM_START) + IM_START
            # c = complex(x/WIDTH*(RE_END - RE_START) + RE_START, y/HEIGHT*(IM_END - IM_START) + IM_START)
            x, y = 0, 0
            iteration = 0
            # while (x*x + y*y) < 4 and iteration < MAX_ITER:
            #     xtemp = x*x -y*y + x0
            #     y = 2*x*y + y0
            #     x=xtemp
            #     iteration += 1
            c = complex(x0, y0)
            z = complex(0,0)
            while abs(z) < 2 and iteration <= MAX_ITER:
                z = z*z +c
                iteration += 1

            if c := abs(z*z) < 2:
                point = pyglet.shapes.Rectangle(Px, Py, 1, 1, color=(0, 0, 0), batch=batch)
                # print(x, y)
                # print(c)
                esta.append(point)

current_time = time()
mandelbrot_set(plane)
print(time()-current_time)
# esta = []
for i in range(20):
    for j in range(20):
        point = pyglet.shapes.Rectangle(i, j, 1, 1, color=(200, 20, 100), batch=batch)
        # esta.append(point)

@window.event
def on_draw():
    window.clear()
    batch.draw()

if __name__ == '__main__':
    pyglet.app.run()

