import ctypes
import platform
import pyglet

# set process DPI aware
def set_process_dpi_aware():
    system = platform.uname()
    if system.system == 'Windows' and float(system.release) > 6:
        ctypes.windll.user32.SetProcessDPIAware()
set_process_dpi_aware()

# basic setup

WIDTH = 720
HEIGHT = 640

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
batch = pyglet.graphics.Batch()

backgournd = pyglet.shapes.Rectangle(0, 0, WIDTH, HEIGHT, color=(23, 124, 98), batch=batch)

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
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1

def mandelbrot_set(plane):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            c = complex(x/100, y/100)
            def iterate(c, n = 10):
                for i in range(n):
                    if abs(c) > 2:
                        return c
                    c = c*c +c
                return None
            if iterate(c) is not None:
                point = pyglet.shapes.Rectangle(x, y, 2, 2, color=(200, 20, 100), batch=batch)
                # print(x, y)
                plane[x][y] = point
mandelbrot_set(plane)

@window.event
def on_draw():
    window.clear()
    batch.draw()

if __name__ == '__main__':
    pyglet.app.run()

