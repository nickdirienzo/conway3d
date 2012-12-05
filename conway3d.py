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

def RGB_to_GL(r, g, b):
    return (r/255.0, g/255.0, b/255.0)

COLORS = (RGB_to_GL(85,98,112),
          RGB_to_GL(78,205,196),
          RGB_to_GL(199,244,100),
          RGB_to_GL(255,107,107),
          RGB_to_GL(196,77,88)) # http://www.colourlovers.com/palette/1930/cheer_up_emo_kid

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
            color = random.sample(COLORS, 1)[0]
            grid[x][y][z] = Box(xc, yc, zc, box_size, color, GL_QUADS)

mid_x = float((grid[-1][0][0].position[0] + box_size) - grid[0][0][0].position[0]) / 2
mid_y = float((grid[0][-1][0].position[1] + box_size) - grid[0][0][0].position[1]) / 2
mid_z = float((grid[0][0][-1].position[2] - box_size) + grid[0][0][0].position[2]) / 2
print mid_x, mid_y, mid_z
ang = 0
position = [0, 0, -200]

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
    glTranslatef(*position) # 4th
    glRotatef(ang, 1, 0, 0) # 3rd
    glRotatef(ang, 0, 1, 0) # 2nd
    glTranslatef(-mid_x, -mid_y, -mid_z) # 1st
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                grid[x][y][z].draw()
    glPopMatrix()
    ang += 5

def update(t):
    global position
    if keys[pyglet.window.key.UP]:
        position[2] += 5
    if keys[pyglet.window.key.DOWN]:
        position[2] -= 5

pyglet.clock.schedule_interval(update,1/20.0)
pyglet.app.run()
