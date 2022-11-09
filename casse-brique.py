#!/usr/bin/env python3
from tkinter import *
import sys
import os

touches = set()

def enfoncer(event):
    touches.add(event.keysym)

def relacher(event):
    try:
        touches.remove(event.keysym)
    except:
        pass

def replay():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def retry_window(a_gagne: str):
    fen2 = Toplevel(fen1)
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
        c.move(plateforme, -3, 0)
    if "Right" in touches and coords[2] <= 797:
        c.move(plateforme, 3, 0)

def ball_move():
    global dx, dy, del_elt, score, score_text
    deplacer_plateforme()
    (bx1,by1,bx2,by2) = c.coords(ball)
    coord_plat = c.coords(plateforme)

    for line in briques:
        for elt in line:
            if elt not in del_elt:
                coord = c.coords(elt)
                if 42 in c.find_overlapping(coord[0], coord[1], coord[2], coord[3]):
                    dy = -dy
                    c.delete(elt)
                    del_elt.append(elt)
                    score += 1
                    c.itemconfigure(score_text, text="score : "+str(round(score/nb_briques*100, 1))+str("%"))
                    c.itemconfigure(briques_text, text="cassé : "+str(score))
                    if score == nb_briques:
                        print("vous avez gagné")
                        retry_window("gagné")
                        return None


    if bx1 <= 0:
        dx = -dx
    if bx2 >= 800:
        dx = -dx
    if by1 <= 0 or 42 in c.find_overlapping(coord_plat[0], coord_plat[1], coord_plat[2], coord_plat[3]):
        dy = -dy
    if by2 >= 600:
        print("vous avez perdu")
        retry_window("perdu")
        return None
    c.move(ball, dx, dy)
    fen1.after(ball_speed, ball_move)

fen1 = Tk()
fen1.title('spterm')
fen1.geometry("800x600")

dx = dy = 1
ball_speed = 3
del_elt = []
score = 0
nb_briques = 8*5

c = Canvas(fen1, bg='black', height=600, width=800)
c.pack()

plateforme = c.create_rectangle(350, 600, 450, 575, fill='blue')

briques = []
for i in range(8):
    briques.append([])
    for j in range(5):
        briques[-1].append(c.create_rectangle(i*100, j*30, i*100+100, j*30+30, fill='red'))

ball = c.create_oval(375, 275, 425, 325, fill='green')
score_text = c.create_text(700, 550, text="score : 0%", font=('Helvetica 15 bold'), fill='white')
briques_text = c.create_text(700, 500, text="cassé : 0", font=('Helvetica 15 bold'), fill='white')

fen1.bind('<KeyPress>', enfoncer)
fen1.bind('<KeyRelease>', relacher)

ball_move()

fen1.mainloop()
