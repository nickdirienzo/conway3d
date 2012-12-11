import random
import time

import pyglet
from pyglet.gl import *

from models import Box, Grid, Camera, RoundTime

window = pyglet.window.Window()
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

rt = RoundTime(5)

grid_size = 3
box_size = 10
box_spacing = 10
grid = Grid(grid_size, box_size, box_spacing, rt.time)

pos = [0, 0, -((grid_size / 2) * box_size * box_size)]
camera = Camera(pos)

text = pyglet.text.Label('', x=5, y=5, font_name='Arial', font_size=16)

@window.event
def on_draw():
    glViewport(0, 0, window.width, window.height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = float(window.width) / window.height
    gluPerspective(60.0, aspect, 0.1, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(*camera.position) # 4th
    glRotatef(grid.heading[0], 1, 0, 0) # 3rd
    glRotatef(grid.heading[1], 0, 1, 0) # 2nd
    glTranslatef(-grid.mid_x, -grid.mid_y, -grid.mid_z) # 1st
    grid.draw()
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,640,0,480)
    glMatrixMode(GL_MODELVIEW)
    text.text = str(rt)
    text.draw()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y == 1:
        camera.zoom(5)
    if scroll_y == -1:
        camera.zoom(-5)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if dx < 0:
        grid.spin_over_y(-3)
    elif dx > 0:
        grid.spin_over_y(3)
    if dy < 0:
        grid.spin_over_x(-3)
    elif dy > 0:
        grid.spin_over_x(3)

def update(t):
    if keys[pyglet.window.key.UP]:
        grid.spin_over_x(-3)
    if keys[pyglet.window.key.DOWN]:
        grid.spin_over_x(3)
    if keys[pyglet.window.key.LEFT]:
        grid.spin_over_y(-3)
    if keys[pyglet.window.key.RIGHT]:
        grid.spin_over_y(3)
    if keys[pyglet.window.key._1]:
        rt.normal_speed()
        grid.update_rt(rt.time)
    if keys[pyglet.window.key._2]:
        rt.double_speed()
        grid.update_rt(rt.time)
    if keys[pyglet.window.key._3]:
        rt.triple_speed()
        grid.update_rt(rt.time)
    grid.update(t)

pyglet.clock.schedule_interval(update,1/24.0)
pyglet.app.run()
