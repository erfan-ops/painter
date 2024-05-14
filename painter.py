import pygame
import sys
import math
from typing import Self


pygame.init()


class Circle(pygame.rect.Rect):
    def __init__(self, left: float, top: float, width: float, height: float, RotPerSec: float, lock: Self|None):
        super().__init__(left, top, width, height)
        self.centerx0: float = 0
        self.centery0: float = 0
        self.center0: tuple[float, float] = (0, 0)
        self.localCenterX: float = self.centerx
        self.localCenterY: float = self.centery
        self.lastX = self.localCenterX
        self.lastY = self.localCenterY
        self.RadPerSec = math.radians(RotPerSec)
        self.rot = self.RadPerSec
        self.lock = lock
    
    def move(self, origin: tuple[float, float], dt: float):
        self.lastX = self.localCenterX
        self.lastY = self.localCenterY
        self.rot = self.RadPerSec + self.lock.rot
        dt_rot = self.rot * dt
        self.localCenterX -= self.lock.lastX - self.lock.localCenterX
        self.localCenterY -= self.lock.lastY - self.lock.localCenterY
        self.centerx0 = self.localCenterX - origin[0]
        self.centery0 = self.localCenterY - origin[1]
        
        self.localCenterX = self.centerx0*math.cos(dt_rot) - self.centery0*math.sin(dt_rot) + origin[0]
        self.localCenterY = self.centerx0*math.sin(dt_rot) + self.centery0*math.cos(dt_rot) + origin[1]
        
        self.center = (self.localCenterX, self.localCenterY)
    
    
    def set_origin(self, origin: tuple[float, float]):
        self.centerx0: float = self.localCenterX - origin[0]
        self.centery0: float = self.localCenterY - origin[1]
        self.center0: tuple[float, float] = (self.centerx0, self.centery0)


WIDTH, HEIGHT = 1600, 900
HW, HH = WIDTH//2, HEIGHT//2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
TARGET_FPS = 720

bg_color = "#151515"
WHITE = "#dedede"


csize = 20
root = Circle((WIDTH - csize)//2, (HEIGHT - csize)//2, csize, csize, 0, None)

c2: Circle = Circle((WIDTH - csize)//2,
                    (HEIGHT - csize)//2 - 200,
                    csize,
                    csize,
                    90,
                    root)
c2.set_origin((HW, HH))

c3: Circle = Circle((WIDTH - csize)//2,
                    (HEIGHT - csize)//2 - 300,
                    csize,
                    csize,
                    -45,
                    c2)

c4: Circle = Circle((WIDTH - csize)//2,
                    (HEIGHT - csize)//2 - 350,
                    csize,
                    csize,
                    -90,
                    c3)

c5: Circle = Circle((WIDTH - csize)//2,
                    (HEIGHT - csize)//2 - 400,
                    csize,
                    csize,
                    720,
                    c4)

circles: list[Circle] = [root, c2, c3, c4, c5]
circles_len = len(circles)
points: list[tuple[int, int]] = []

# screen.fill(bg_color)
# pygame.display.flip()
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
    
    screen.fill(bg_color)
    
    fps = clock.get_fps()
    dt = clock.get_time() / 1000
    
    pygame.display.set_caption(f"fps: {fps:.2f}")
    
    x, y = HW, HH
    
    for i, circle in enumerate(circles):
        pygame.draw.ellipse(screen, WHITE, circle)
        
        if i > 0:
            pygame.draw.line(screen, WHITE, circle.center, circles[i-1].center, 5)
            circle.move((x, y), dt)
            x += circle.centerx0
            y += circle.centery0
    
    points.append(circles[-1].center)
    
    for point in points:
        rect = (*point, 4, 4)
        pygame.draw.rect(screen, WHITE, rect)
    
    # rect3 = pygame.draw.line(screen, WHITE, circles[-1].center, circles[-2].center, 2)
    
    # pygame.display.update(rect3)
    pygame.display.flip()
    clock.tick(TARGET_FPS)


pygame.quit()
sys.exit()
