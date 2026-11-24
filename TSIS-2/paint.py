import pygame
from datetime import datetime
from pathlib import Path
from tools import shape, flood_fill

pygame.init()
W,H,TOP=1000,720,132
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption('TSIS 2 | Paint')
canvas=pygame.Surface((W,H-TOP))
canvas.fill('white')
font=pygame.font.Font(None,23)
text_font=pygame.font.Font(None,32)
clock=pygame.time.Clock()
tools=['Pencil','Line','Rectangle','Circle','Square','Right triangle','Equilateral','Rhombus','Eraser','Fill','Text','Picker']
buttons=[(name,pygame.Rect(8+i%6*164,8+i//6*32,158,28)) for i,name in enumerate(tools)]
colors=[(0,0,0),(230,40,50),(35,100,220),(20,160,80),(245,190,30),(150,65,190),(255,255,255)]
tool='Pencil'; color=colors[0]; width=5
start=last=None
text_pos=None; typed=''; status='Ctrl+S / Cmd+S: save PNG'
running=True

def point(pos):
    return (max(0,min(W-1,pos[0])),max(0,min(H-TOP-1,pos[1]-TOP)))

def save():
    folder=Path(__file__).resolve().parent/'saves'
    folder.mkdir(exist_ok=True)
    path=folder/datetime.now().strftime('paint_%Y%m%d_%H%M%S_%f.png')
    pygame.image.save(canvas,str(path))
    return 'Saved: '+path.name

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_s and event.mod & (pygame.KMOD_CTRL|pygame.KMOD_META):
                status=save()
            elif text_pos is not None:
                if event.key==pygame.K_RETURN:
                    canvas.blit(text_font.render(typed,True,color),text_pos)
                    text_pos=None; typed=''; pygame.key.stop_text_input()
                elif event.key==pygame.K_ESCAPE:
                    text_pos=None; typed=''; pygame.key.stop_text_input()
                elif event.key==pygame.K_BACKSPACE:
                    typed=typed[:-1]
            elif event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                width={pygame.K_1:2,pygame.K_2:5,pygame.K_3:10}[event.key]
        elif event.type==pygame.TEXTINPUT and text_pos is not None:
            typed+=event.text
        elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if event.pos[1]<TOP:
                for name,rect in buttons:
                    if rect.collidepoint(event.pos):
                        tool=name; text_pos=None; typed=''; pygame.key.stop_text_input()
                for i,c in enumerate(colors):
                    if pygame.Rect(8+i*34,76,30,28).collidepoint(event.pos): color=c
                for i,s in enumerate((2,5,10)):
                    if pygame.Rect(270+i*80,76,75,28).collidepoint(event.pos): width=s
                if pygame.Rect(520,76,100,28).collidepoint(event.pos): status=save()
            else:
                p=point(event.pos)
                if tool=='Fill': flood_fill(canvas,p,color)
                elif tool=='Picker': color=tuple(canvas.get_at(p))[:3]
                elif tool=='Text':
                    text_pos=p; typed=''; pygame.key.start_text_input()
                else:
                    start=last=p
                    if tool in ('Pencil','Eraser'):
                        pygame.draw.circle(canvas,color if tool=='Pencil' else 'white',p,max(1,width//2))
        elif event.type==pygame.MOUSEMOTION and start is not None and tool in ('Pencil','Eraser'):
            p=point(event.pos)
            pygame.draw.line(canvas,color if tool=='Pencil' else 'white',last,p,width)
            last=p
        elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and start is not None:
            if tool not in ('Pencil','Eraser'):
                shape(canvas,tool,start,point(event.pos),color,width)
            start=last=None
    screen.fill((35,43,60))
    screen.blit(canvas,(0,TOP))
    if start is not None and tool not in ('Pencil','Eraser'):
        preview=canvas.copy()
        shape(preview,tool,start,point(pygame.mouse.get_pos()),color,width)
        screen.blit(preview,(0,TOP))
    if text_pos is not None:
        preview=canvas.copy()
        label=text_font.render(typed+'|',True,color)
        preview.blit(label,text_pos)
        screen.blit(preview,(0,TOP))
    for name,rect in buttons:
        pygame.draw.rect(screen,(45,110,200) if name==tool else (65,75,95),rect,border_radius=5)
        screen.blit(font.render(name,True,'white'),(rect.x+8,rect.y+5))
    for i,c in enumerate(colors):
        rect=pygame.Rect(8+i*34,76,30,28)
        pygame.draw.rect(screen,c,rect)
        pygame.draw.rect(screen,'white' if c==color else (100,100,100),rect,3 if c==color else 1)
    for i,s in enumerate((2,5,10)):
        rect=pygame.Rect(270+i*80,76,75,28)
        pygame.draw.rect(screen,(45,110,200) if s==width else (65,75,95),rect,border_radius=5)
        screen.blit(font.render(f'{s} px',True,'white'),(rect.x+12,rect.y+5))
    pygame.draw.rect(screen,(45,110,200),(520,76,100,28),border_radius=5)
    screen.blit(font.render('Save PNG',True,'white'),(530,81))
    screen.blit(font.render(status,True,'white'),(8,110))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
