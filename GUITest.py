# -*- coding: UTF-8 -*-
 
import tkinter as tk           # 导入 Tkinter 库
import math
import random

root = tk.Tk()                     # 创建窗口对象的背景色
root.title("Star go!")
root.geometry('620x520')

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vel:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Star():
    def __init__(self, s, pos, r, m, v):
        self.s = s
        self.pos = pos
        self.r = r
        self.m = m
        self.v = v

WEIGHT = 10000
WIDTH = 500
HEIGHT = 500
R = 8
G = 1

stars = []
stoped = True

def getdis(x1, x2, y1, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def creat_star(x, y, r, v=Vel(0,0), m = WEIGHT):
    s = cv.create_oval(x - r, y - r, x + r, y + r)
    s_tmp = Star(s, Pos(x, y), r, m, v)
    stars.append(s_tmp)

def force(star1, star2):
    plus = -1
    x = star1.pos.x - star2.pos.x
    y = star1.pos.y - star2.pos.y
    dis = x*x + y*y
    if dis == 0:
        return
    if math.sqrt(dis) < star1.r + star2.r :
        plus = (star1.r + star2.r) / math.sqrt(dis)
        dis = (star1.r + star2.r) ** 2
    f = G * star1.m * star2.m / dis
    fx = f / math.sqrt(dis) * x
    fy = f / math.sqrt(dis) * y
    return [fx * plus, fy * plus]

def clickpause():
    global moving
    global stoped
    stoped = True
    root.after_cancel(moving)
    cmd["text"] = "Start move!"
    cmd["command"] = clickmove
    root.update()

def clickmove():
    global stoped
    stoped = False
    movethem()
    cmd["text"] = "Pause!"
    cmd["command"] = clickpause
    root.update()


def movethem():
    for star in stars:
        for oth in stars:
            if star.s != oth.s:
                f = force(star, oth)
                star.v.x += f[0] / star.m
                star.v.y += f[1] / star.m
                if star.v.x >= 50:
                    star.v.x = (star.v.x - 50) * 0.1 + 40
                if star.v.y >= 50:
                    star.v.y = (star.v.y - 50) * 0.1 + 40
    for star in stars:
        cv.delete(star.s)
        star.pos.x += star.v.x
        star.pos.y += star.v.y
        if star.pos.x <= 0:
            star.v.x *= -1
            star.pos.x = 1
        if star.pos.x >= WIDTH:
            star.v.x *= -1
            star.pos.x = WIDTH - 1
        if star.pos.y <= 0:
            star.v.y *= -1
            star.pos.y = 1
        if star.pos.y >= HEIGHT:
            star.v.y *= -1
            star.pos.y = HEIGHT - 1
    for star in stars:
        star.s = cv.create_oval(star.pos.x - star.r, star.pos.y - star.r, star.pos.x + star.r, star.pos.y + star.r)
        #print("moved star", star.s)
    global moving
    moving = root.after(40, movethem)

def stopall():
    for star in stars:
        star.v = Vel(0,0)

cv = tk.Canvas(root, bg='skyblue', height=HEIGHT, width=WIDTH)
cmd = tk.Button(root, text="Start move!", width=15, height=2, command=clickmove)
tst = tk.Button(root, text="Kill Velocity", width=15, height=2, command=stopall)

creat_star(200,200,10*R,Vel(0,0),)
creat_star(200,400,R,Vel(5,0),0.001)
creat_star(100,400,R,Vel(5,0),0.001)
creat_star(300,400,R,Vel(5,0),0.001)



cv.place(x=5, y=5)
cmd.place(x=505 + 10, y=5)
tst.place(x=505 + 10, y=55)

root.mainloop()
