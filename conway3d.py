import random
import euclid
import pyglet
from pyglet.gl import *

window = pyglet.window.Window()
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
glEnable(pyglet.gl.GL_DEPTH_TEST)

fovy = 60.0
GRID_SIZE = 4
grid = [[[0] * GRID_SIZE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

class Box(object):
    def __init__(self, x, y, z, size, color, render_type):
        self.position = euclid.Vector3(x, y, z)
        self.color = color
        self.size = size
        self.rt = render_type

    def draw(self):
        x, y, z = self.position
        glPushMatrix()
        glColor3f(self.color[0], self.color[1], self.color[2])
        glTranslatef(x, y, z)
        # Front face
        glBegin(self.rt)
        glVertex3f(0, 0, 0)
        glVertex3f(self.size, 0, 0)
        glVertex3f(self.size, self.size, 0)
        glVertex3f(0, self.size, 0)
        glEnd()
        # Left face
        glBegin(self.rt)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, -self.size)
        glVertex3f(0, self.size, -self.size)
        glVertex3f(0, self.size, 0)
        glEnd()
        # Back face
        glBegin(self.rt)
        glVertex3f(0, 0, -self.size)
        glVertex3f(0, self.size, -self.size)
        glVertex3f(self.size, self.size, -self.size)
        glVertex3f(self.size, 0, -self.size)
        glEnd()
        # Right face
        glBegin(self.rt)
        glVertex3f(self.size, 0, 0)
        glVertex3f(self.size, self.size, 0)
        glVertex3f(self.size, self.size, -self.size)
        glVertex3f(self.size, 0, -self.size)
        glEnd()
        # Top face
        glBegin(self.rt)
        glVertex3f(0, self.size, 0)
        glVertex3f(0, self.size, -self.size)
        glVertex3f(self.size, self.size, -self.size)
        glVertex3f(self.size, self.size, 0)
        glEnd()
        # Bottom face
        glBegin(self.rt)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, -self.size)
        glVertex3f(self.size, 0, -self.size)
        glVertex3f(self.size, 0, 0)
        glEnd()
        glPopMatrix()

mid_x = (GRID_SIZE * 20) / 2
mid_y = (GRID_SIZE * 20) / 2
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        for z in range(GRID_SIZE):
            xc = (x * 20) #- mid_x
            yc = (y * 20) #- mid_y
            zc = (-1 * z * 20) - 100
            grid[x][y][z] = Box(xc, yc, zc, 10, (random.random(), random.random(), 1), GL_QUADS)

grid[0][0][0].color = (1, 0, 0)

@window.event
def on_draw():
    glViewport(0, 0, window.width, window.height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(window.width) / window.height
    gluPerspective(fovy, aspect, 0.1, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-mid_x, -mid_y, -50)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                grid[x][y][z].draw()
    glBegin(GL_LINES)
    glVertex3f(mid_x, -100, 0)
    glVertex3f(mid_x, 100, 0)
    glEnd()
def update(t):
    global fovy
    if keys[pyglet.window.key.UP]:
        fovy -= 1
    if keys[pyglet.window.key.DOWN]:
        fovy += 1
pyglet.clock.schedule_interval(update,1/20.0)
pyglet.app.run()
