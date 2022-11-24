#!/usr/bin/env python3
from tkinter import *
import sys
import os

#~ Customisation ~#
use_cursor       = True
color_briques    = 'purple'
color_plateforme = 'blue'
color_ball       = 'orange'
ball_diameter    = 30
plateforme_long  = 100
ball_speed       = 1
speed_plat       = 3
#~ Customisation ~#

def enfoncer(event):
    touches.add(event.keysym)

def relacher(event):
    try:
        touches.remove(event.keysym)
    except:
        pass

def replay(arg=0):
    python = sys.executable
    os.execl(python, python, * sys.argv)

def start_ball(arg=0):
    global dx, dy, speed_plat
    if dx == 0 and dy == 0:
        dx, dy = last_state
        speed_plat = 3
    else:
        dx = dy = 0
        speed_plat = 0

def retry_window(a_gagne: str):
    fen2 = Toplevel(fen1)
    fen2.bind('r', replay)
    fen2.bind('q', quit)
    lbl1 = Label(fen2, text="Vous avez "+a_gagne)
    lbl1.pack(side=TOP)
    lbl2 = Label(fen2, text="Relancer ?")
    lbl2.pack(pady=10)

    btn_replay = Button(fen2, text='Oui', command=replay)
    btn_replay.pack(side=LEFT)

    btn_quit = Button(fen2, text='Non', command=fen1.destroy)
    btn_quit.pack(side=RIGHT)

def deplacer_plateforme():
    coords = c.coords(plateforme)
    if 'Left' in touches and coords[0] >= 3:
        c.move(plateforme, -speed_plat, 0)
    if "Right" in touches and coords[2] <= 797:
        c.move(plateforme, speed_plat, 0)

def ball_move():
    global del_elt, score, score_text, dx, dy, last_state
    if dx != 0 or dy != 0:
        last_state = (dx, dy)
    deplacer_plateforme()
    (bx1,by1,bx2,by2) = c.coords(ball)
    coord_plat = c.coords(plateforme)
    coord_ball = c.coords(ball)

    for line in briques:
        for elt in line:
            if elt not in del_elt:
                coord = c.coords(elt)
                if ball in c.find_overlapping(*coord):
                    dy = -dy
                    c.delete(elt)
                    del_elt.append(elt)
                    score += 1
                    c.itemconfigure(score_text, text="score : "+str(round(score/nb_briques*100, 1))+str("%"))
                    c.itemconfigure(briques_text, text="cassé : "+str(score))
                    if score == nb_briques:
                        retry_window("gagné")
                        return None

    if bx1 <= 0:
        dx = -dx
    if bx2 >= 800:
        dx = -dx
    if by1 <= 0 or ball in c.find_overlapping(*coord_plat):
        dy = -dy
        c.coords(ball, coord_ball[0]-1, coord_ball[1]-1, coord_ball[2]-1, coord_ball[3]-1)
    if by2 >= 600:
        retry_window("perdu")
        return None
    c.move(ball, dx, dy)
    fen1.after(3, ball_move)

def fill_line(i, dec):
    color = 'red'
    tab = []
    if dec == 50:
        tab.append(c.create_rectangle(0, i*30, 50, i*30+30, fill=color_briques))
    else:
        tab.append(c.create_rectangle(0, i*30, 100, i*30+30, fill=color_briques))
    for j in range(dec, 700+dec, 100):
        tab.append(c.create_rectangle(j, i*30, j+100, i*30+30, fill=color_briques))
    if dec == 50:
        tab.append(c.create_rectangle(750, i*30, 800, i*30+30, fill=color_briques))
    return tab

def f(event):
    if use_cursor:
        c.coords(plateforme, event.x-50, 590, event.x+50, 580)

touches = set()
fen1 = Tk()
fen1.title('spterm')
fen1.geometry("800x600")

dx = dy = 0
last_state = (ball_speed, ball_speed)
del_elt = []
score = 0
colors = 'red'
alt = 1

c = Canvas(fen1, bg='black', height=600, width=800)
c.pack()

plateforme = c.create_rectangle(400-plateforme_long//2, 590, 400+plateforme_long//2, 580, fill=color_plateforme)

briques = []

for i in range(5):
    line = fill_line(i, (alt%2)*50+50)
    briques.append(line)
    alt += 1

nb_briques = sum([len(i) for i in briques])

ball = c.create_oval(400-ball_diameter//2, 300-ball_diameter//2, 400+ball_diameter//2, 300+ball_diameter//2, fill=color_ball)
score_text = c.create_text(700, 550, text="score : 0%", font=('Helvetica 15 bold'), fill='white')
briques_text = c.create_text(700, 500, text="cassé : 0", font=('Helvetica 15 bold'), fill='white')

fen1.bind('<KeyPress>', enfoncer)
fen1.bind('<KeyRelease>', relacher)
fen1.bind('p', start_ball)
fen1.bind('r', replay)
fen1.bind('q', quit)
fen1.bind('<Motion>', f)

ball_move()

fen1.mainloop()
