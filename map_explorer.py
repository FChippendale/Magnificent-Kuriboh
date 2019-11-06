import pygame, sys, math
import numpy as np


colours = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255))


def rotate2d(pos, rad):
    x,y = pos 
    s,c = math.sin(rad), math.cos(rad)
    return x*c - y*s, y*c + x*s 
    
def apply_transform(x,y,z):
    x -= cam.pos[0]
    y -= cam.pos[1]
    z -= cam.pos[2]

    x,z = rotate2d((x,z), cam.rot[1])
    y,z = rotate2d((y,z), cam.rot[0])

    f = 200/z
    x,y = x*f, y*f
    return [(cx + int(x), cy + int(y))]

class Cam:
    def __init__(self, pos = (0, 0, 0), rot = (0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
    
    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x /= 200
            y /= 200
            self.rot[0] += y
            self.rot[1] += x
        
    def update(self,dt,key):
        s = dt*10
        
        if key[pygame.K_q]: self.pos[1] += s
        if key[pygame.K_e]: self.pos[1] -= s
            
        x,y = s * math.sin(self.rot[1]), s * math.cos(self.rot[1])
        
        if key[pygame.K_w]: self.pos[0] += x; self.pos[2] += y
        if key[pygame.K_s]: self.pos[0] -= x; self.pos[2] -= y
            
        if key[pygame.K_a]: self.pos[0] -= y; self.pos[2] += x
        if key[pygame.K_d]: self.pos[0] += y; self.pos[2] -= x
            
        



pygame.init()
w,h = 400, 400
cx, cy = w//2, h//2
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Magnificent Kuriboh")
clock = pygame.time.Clock()

walls = []
level_layout =  open('level_layout.txt', 'r')
for i, wall in enumerate(level_layout):
    walls.append(list((((int(wall[0:3]) + int(wall[8:11])) ** 2 + (int(wall[4:7]) + int(wall[12:15])) ** 2) ** 0.5 * 2, int(wall[0:3]), int(wall[4:7]), int(wall[8:11]), int(wall[12:15]), i)))
walls.sort(reverse = True)
    
cam = Cam(pos = (0,0,-6))

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

        
while True:
    dt = clock.tick()/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(), sys.exit()
        cam.events(event)
        
    screen.fill((255, 255, 255))
    
    
    for wall in walls:
        wall[0] = (((wall[1] + wall[2])/2 - cam.pos[0]) ** 2 + ((wall[3] + wall[4])/2 - cam.pos[2]) ** 2) ** 0.5
        
    walls.sort(reverse = True)
    
    for wall in walls:
        points = []
        (_, x1, z1, x2, z2, _) = wall
        y1 = 2
        y2 = -2
        points += apply_transform(x1, y1, z1)
        points += apply_transform(x1, y2, z1)
        points += apply_transform(x2, y2, z2)
        points += apply_transform(x2, y1, z2)
        
        off_screen = False
        for i in points:
            if i[0] < -300 or i[0] > 700 or i[1] < -300 or i[1] > 700:
                 off_screen = True
        
        if not off_screen:
            pygame.draw.polygon(screen, colours[wall[5] % len(colours)], points)
        
        
    pygame.display.flip()
    
    key = pygame.key.get_pressed()
    cam.update(dt, key)
