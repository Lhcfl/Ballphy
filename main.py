# -*- coding: UTF-8 -*-
 
import tkinter as tk           # 导入 Tkinter 库
import math
import random

class Group():
    # 数据组 父类
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    def __add__(self, b):
        if isinstance(b, Group):
            return type(self)(self.x + b.x, self.y + b.y)
        else:
            return NotImplemented
    def __sub__(self, b):
        if isinstance(b, Group):
            return type(self)(self.x - b.x, self.y - b.y)
        else:
            return NotImplemented

class Vect(Group):
    # 向量 子类
    def __init__(self, x, y):
        super().__init__(x, y)
    def __mul__(self, b):
        if isinstance(b, Group):
            return self.x*b.x+self.y*b.y
        else:
            return type(self)(self.x * b, self.y * b)
    def __rmul__(self, a):
        return type(self)(self.x * a, self.y * a)

class Pos(Group):
    # 坐标 子类
    def __init__(self, x, y):
        super().__init__(x, y)

class Vel(Vect):
    # 速度 子类
    def __init__(self, x, y):
        super().__init__(x, y)

class Ball():
    def __init__(self, ID, pos, r, v, m):
        self.ID=ID
        self.pos=pos
        self.r=r
        self.v=v
        self.m=m
    def moveto(pos):
        self.pos=pos
    def move(pos):
        self.pos+=self.v

class Timer():
    # 计时器
    def __init__(self, root, func, time, enabled):
        self.rt = root
        self.func = func
        self.t=time
        self.enabled=enabled
        if enabled:
            self.enable()
    def timeup():
        func()
    def enable():
        self.enabled = True
        self.ti = rt.after(time, self.timeup)
    def unable():
        self.enabled = False
        rt.after_cancel(self.ti)

class ID_Pool():
    # ID池
    def __init__(self):
        self.pool=[]
        self.topid=0
    def getid(self):
        if len(self.pool) == 0:
            self.topid+=1
            return self.topid
        else:
            return self.pool.pop()
    def back(self, p):
        self.pool.append(p)

balls = []
DeadTime = 1e7
CountNum = 0
root = tk.Tk()                 
root.title("Star go!")
root.geometry('620x520')

def draw_ball(ball):
    pass

def creat_ball(ball):
    pass

def del_ball(ball):
    pass

def update():
    pass

def hited(b1, b2):
    pass

def count_hit():
    pass

def hit(b1, b2):
    pass

def dis(p1, p2):
    pass

def move():
    pass

def update():
    #更新整个画布
    pass

def main_loop():
    pass

cv = tk.Canvas(root, bg='skyblue', height=HEIGHT, width=WIDTH)
#cmd = tk.Button(root, text="Start move!", width=15, height=2, command=clickmove)
#tst = tk.Button(root, text="Kill Velocity", width=15, height=2, command=stopall)

#creat_star(200,200,10*R,Vel(0,0),)
#creat_star(200,400,R,Vel(5,0),0.001)
#creat_star(100,400,R,Vel(5,0),0.001)
#creat_star(300,400,R,Vel(5,0),0.001)



cv.place(x=5, y=5)
#cmd.place(x=505 + 10, y=5)
#tst.place(x=505 + 10, y=55)

root.mainloop()

