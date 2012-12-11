import random
import time

import pyglet
from pyglet.gl import *

class ColorPalette(object):
    def __init__(self):
        self.colors = (
                self.RGB_to_GL(85,98,112),
                self.RGB_to_GL(78,205,196),
                self.RGB_to_GL(199,244,100),
                self.RGB_to_GL(255,107,107),
                self.RGB_to_GL(196,77,88)
                ) # http://www.colourlovers.com/palette/1930/cheer_up_emo_kid

    def RGB_to_GL(self, r, g, b):
        return (r/255.0, g/255.0, b/255.0)

class Camera(object):
    def __init__(self, pos):
        self.position = pos

    def zoom(self, z):
        self.position[2] += z

class Box(object):
    def __init__(self, x, y, z, size, color, render_type, alive):
        self.position = [x, y, z]
        self.alive_color = color
        self.dead_color = (1, 1, 1)
        self.cur_color = color 
        self.size = size
        self.rt = render_type
        self.alive = alive
        self.color_change_duration = 5
        self.start_time = time.time()

    def update(self, dt):
        temp = list()
        t = time.time() - self.start_time
        if t <= self.color_change_duration:
            a = t / self.color_change_duration
            if self.alive:
                for i in range(len(self.cur_color)):
                    temp.append((1 - a) * self.alive_color[i] + a * self.dead_color[i])
                    self.cur_color = tuple(temp)
            else:
                for i in range(len(self.cur_color)):
                    temp.append((1 - a) * self.dead_color[i] + a * self.alive_color[i])
                    self.cur_color = tuple(temp)
        else:
            a = 0

    def draw(self):
        x, y, z = self.position
        glPushMatrix()
        glColor3f(self.cur_color[0], self.cur_color[1], self.cur_color[2])
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

class Grid(object):
    
    def __init__(self, size, box_size, box_spacing):
        self.size = size
        self.box_size = box_size
        self.box_spacing = box_spacing
        self.grid = [[[0] * self.size for _ in range(self.size)] for _ in range(self.size)]
        palette = ColorPalette()
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    xc = (x * (self.box_size + self.box_spacing))
                    yc = (y * (self.box_size + self.box_spacing))
                    zc = (-1 * z * (self.box_size + self.box_spacing)) - 100
                    color = random.sample(palette.colors, 1)[0]
                    self.grid[x][y][z] = Box(xc, yc, zc, self.box_size, color, GL_QUADS, random.random() < 0.4)
        self.mid_x = float((self.grid[-1][0][0].position[0] + self.box_size) - self.grid[0][0][0].position[0]) / 2
        self.mid_y = float((self.grid[0][-1][0].position[1] + self.box_size) - self.grid[0][0][0].position[1]) / 2
        self.mid_z = float((self.grid[0][0][-1].position[2] - self.box_size) + self.grid[0][0][0].position[2]) / 2
        self.heading = [0, 0]

    def draw(self):
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    self.grid[x][y][z].draw()

    def update(self, t):
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    self.grid[x][y][z].update(t)

    def spin_over_x(self, x):
        self.heading[0] += x
    
    def spin_over_y(self, y):
        self.heading[1] += y

