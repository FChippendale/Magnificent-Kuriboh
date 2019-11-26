from OpenGL.GL import *
from OpenGL.GL import shaders
import pygame
from pygame.locals import *
import numpy as np
import sys
import ctypes

pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glClear(GL_COLOR_BUFFER_BIT)

triangle = [-0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0,
            0.5, -0.5, 0.0,
            1.5, -0.5, 0.0,
            1.0, 0.5, 0.0]

triangle = np.array(triangle, dtype = np.float32)

colors = [0.0, 0.0, 1.0, 
          0.0, 0.0, 1.0, 
          0.0, 0.0, 1.0, 
          0.0, 1.0, 0.0, 
          0.0, 1.0, 0.0, 
          0.0, 1.0, 0.0]

colors = np.array(colors, dtype = np.float32)

vertex_shader = """
#version 330
in vec4 position;
in vec4 color;
out vec4 color_from_vshader;

void main()
{
    gl_Position = position;
    color_from_vshader = color;
}
"""

fragment_shader = """
#version 330

in vec4 color_from_vshader;

void main()
{
    gl_FragColor = color_from_vshader;
}
"""
shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER), OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(triangle) + sys.getsizeof(colors), None, GL_STATIC_DRAW) 
glBufferSubData(GL_ARRAY_BUFFER, 0, sys.getsizeof(triangle), triangle)
glBufferSubData(GL_ARRAY_BUFFER, sys.getsizeof(triangle), sys.getsizeof(colors), colors)

position = glGetAttribLocation(shader, "position")
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)

color_attribute = glGetAttribLocation(shader, "color")
glVertexAttribPointer(color_attribute, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(sys.getsizeof(triangle)))
glEnableVertexAttribArray(color_attribute)


glEnableVertexAttribArray(position)

glUseProgram(shader)

glDrawArrays(GL_TRIANGLES, 0, 6) #last variable is number of triangles
pygame.display.flip()
pygame.time.wait(10000)

pygame.quit()
sys.exit()
