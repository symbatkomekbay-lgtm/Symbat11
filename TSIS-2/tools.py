import pygame
from collections import deque
import math

def flood_fill(surface, pos, color):
    """Fill connected pixels of exactly the same color."""
    w, h = surface.get_size()
    x, y = pos
    if not (0 <= x < w and 0 <= y < h):
        return
    old = surface.get_at(pos)
    color = pygame.Color(*color)
    if old == color:
        return
    queue = deque([pos])
    surface.set_at(pos, color)
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and surface.get_at((nx,ny)) == old:
                surface.set_at((nx,ny), color)
                queue.append((nx,ny))

def shape(surface, tool, a, b, color, width):
    x,y = a
    u,v = b
    l,t = min(x,u),min(y,v)
    w,h = abs(u-x),abs(v-y)
    if tool == 'Line':
        pygame.draw.line(surface,color,a,b,width)
    elif tool == 'Rectangle':
        pygame.draw.rect(surface,color,(l,t,w,h),width)
    elif tool == 'Circle':
        pygame.draw.circle(surface,color,a,int(math.hypot(u-x,v-y)),width)
    elif tool == 'Square':
        s=min(w,h)
        pygame.draw.rect(surface,color,(x if u>=x else x-s,y if v>=y else y-s,s,s),width)
    elif tool == 'Right triangle':
        pygame.draw.polygon(surface,color,[(x,y),(x,v),(u,v)],width)
    elif tool == 'Equilateral':
        s=min(w,int(h*2/math.sqrt(3)))
        hh=round(s*math.sqrt(3)/2)
        pygame.draw.polygon(surface,color,[(l+s//2,t),(l,t+hh),(l+s,t+hh)],width)
    elif tool == 'Rhombus':
        pygame.draw.polygon(surface,color,[(l+w//2,t),(l+w,t+h//2),(l+w//2,t+h),(l,t+h//2)],width)
