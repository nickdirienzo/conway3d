import random
import euclid
import pyglet
from pyglet.gl import *

window = pyglet.window.Window()
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
glEnable(pyglet.gl.GL_DEPTH_TEST)

fovy = 60.0
GRID_SIZE = 5
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

box_size = 10
padding = 10
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        for z in range(GRID_SIZE):
            xc = (x * (box_size + padding))
            yc = (y * (box_size + padding))
            zc = (-1 * z * (box_size + padding)) - 100
            grid[x][y][z] = Box(xc, yc, zc, box_size, (random.random(), random.random(), 1), GL_QUADS)

mid_x = float((grid[-1][0][0].position[0] + box_size) - grid[0][0][0].position[0]) / 2
mid_y = float((grid[0][-1][0].position[1] + box_size) - grid[0][0][0].position[1]) / 2
mid_z = float((grid[0][0][-1].position[2] - box_size) + grid[0][0][0].position[2]) / 2
print mid_x, mid_y, mid_z
ang = 0

@window.event
def on_draw():
    global ang
    glViewport(0, 0, window.width, window.height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(window.width) / window.height
    gluPerspective(fovy, aspect, 0.1, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(0, 0, -200)
    glRotatef(ang, 1, 0, 0)
    glRotatef(ang, 0, 1, 0)
    glTranslatef(-mid_x, -mid_y, -mid_z)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                grid[x][y][z].draw()
    glPopMatrix()
    ang += 5

def update(t):
    global fovy, rotate
    if keys[pyglet.window.key.UP]:
        fovy -= 1
    if keys[pyglet.window.key.DOWN]:
        fovy += 1

pyglet.clock.schedule_interval(update,1/20.0)
pyglet.app.run()
