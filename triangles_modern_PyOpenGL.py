from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import pygame
from pygame.locals import *
import numpy as np
import sys
import ctypes

def Rotate(x_theta, y_theta, z_theta):
    x_rot_matrix = np.array([[1, 0, 0, 0],
                             [0, np.cos(x_theta), -np.sin(x_theta), 0],
                             [0, np.sin(x_theta), np.cos(x_theta), 0],
                             [0, 0, 0, 1]])
    
    y_rot_matrix = np.array([[np.cos(y_theta), 0, np.sin(y_theta), 0],
                             [0, 1, 0, 0],
                             [-np.sin(y_theta), 0, np.cos(y_theta), 0],
                             [0, 0, 0, 1]])
    
    z_rot_matrix = np.array([[np.cos(z_theta), -np.sin(z_theta), 0, 0],
                             [np.sin(z_theta), np.cos(z_theta), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]])
    return np.matmul(x_rot_matrix, np.matmul(y_rot_matrix, z_rot_matrix))

def Translation(dx, dy, dz):
    translation_matrix = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0], 
                                   [0, 0, 1, 0],
                                   [dx, dy, dz, 1]])
    return translation_matrix

def Perspective(alpha):
    NearZ = 0.1
    FarZ = 50
    persp_matrix = np.array([[1/(display[0]/display[1] * np.tan(alpha / 2)), 0, 0, 0],
                             [0, 1/np.tan(alpha / 2), 0, 0], 
                             [0, 0, (-NearZ-FarZ)/(NearZ-FarZ), 2 * NearZ * FarZ / (NearZ-FarZ)],
                             [0, 0, 1, 0]])
    return persp_matrix
    

def loadImage():
    img = pygame.image.load("Texture_Test.png")
    textureData = pygame.image.tostring(img, "RGB", 1)
    width = img.get_width()
    height = img.get_height()
    bgImgGL = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, bgImgGL)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
    glEnable(GL_TEXTURE_2D)
    
    

pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

mouseMove = (0, 0)
prev_mouseMove = (0, 0)
up_down_mouseMove = 0

triangle = [-1.0, -0.5, 0.0,
            1.0, -0.5, 0.0,
            -1.0, 0.5, 0.0]

triangle = np.array(triangle, dtype = np.float32)

colors = [0.0, 0.0, 1.0, 
          0.0, 0.0, 1.0, 
          0.0, 0.0, 1.0]

colors = np.array(colors, dtype = np.float32)

v_shader = """
#version 330
in vec4 position;
in vec3 color;

uniform mat4 view_matrix;

out vec3 color_from_vshader;


void main()
{
    gl_Position = view_matrix * position;
    color_from_vshader = color;
}
"""

f_shader = """
#version 330

in vec3 color_from_vshader;

void main()
{
    gl_FragColor = vec4(color_from_vshader, 1.0f);
}
"""
vertex_shader = OpenGL.GL.shaders.compileShader(v_shader, GL_VERTEX_SHADER)
fragment_shader = OpenGL.GL.shaders.compileShader(f_shader, GL_FRAGMENT_SHADER)
shader = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(triangle) + sys.getsizeof(colors), None, GL_DYNAMIC_DRAW) 
glBufferSubData(GL_ARRAY_BUFFER, 0, sys.getsizeof(triangle), triangle)
glBufferSubData(GL_ARRAY_BUFFER, sys.getsizeof(triangle), sys.getsizeof(colors), colors)

position = glGetAttribLocation(shader, "position")
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(position)

view_matrix = glGetUniformLocation(shader, "view_matrix")

color_attribute = glGetAttribLocation(shader, "color")
glVertexAttribPointer(color_attribute, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(sys.getsizeof(triangle)))
glEnableVertexAttribArray(color_attribute)

glUseProgram(shader)


cur_pos = [0, -8] #X Z

while True:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
        if event.type == pygame.MOUSEMOTION:
            mouseMove = event.rel
                
               
    if mouseMove[0] == prev_mouseMove[0]:
        mouseMove = (0, mouseMove[1])
    if mouseMove[1] == prev_mouseMove[1]:
        mouseMove = (mouseMove[0], 0)    
    up_down_mouseMove += mouseMove[1]
        
    prev_mouseMove = mouseMove
    
    keypress = pygame.key.get_pressed() 



    # apply the movment 
    if keypress[pygame.K_w]:
        cur_pos[1] += 0.1
    if keypress[pygame.K_s]:
        cur_pos[1] -= 0.1
    if keypress[pygame.K_d]:
        cur_pos[0] += 0.1
    if keypress[pygame.K_a]:
        cur_pos[0] -= 0.1
    


    
    viewMatrix = np.matmul(Translation(cur_pos[0], 0, cur_pos[1]), Rotate(0, up_down_mouseMove * 0.1, mouseMove[0] * 0.1))
    viewMatrix = np.matmul(Perspective(np.pi / 4), viewMatrix)
    
    glUniformMatrix4fv(view_matrix, 1, GL_FALSE, viewMatrix)
    
    
    glDrawArrays(GL_TRIANGLES, 0, 6) #last variable is number of points of triangles
    

    pygame.display.flip()
    pygame.time.wait(10)
    
    
