#!/usr/bin/python3
# -*- coding: UTF-8 -*- 

import tkinter as tk           # 导入 Tkinter 库
import math
import random

class Pair():
    # 数据组
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __lt__(self, b):
        if isinstance(b, Pair):
            return self.x < b.x
        else:
            return NotImplemented

class Group(Pair):
    # 浮点数据组类
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = float(self.x)
        self.y = float(self.y)
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
    def mod(self):
        return math.sqrt(self.x*self.x+self.y*self.y)
    def __lt__(self, b):
        if isinstance(b, Group):
            return self.x < b.x
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
    def __init__(self, ID, pos, r=10, v = Vel(0,0), m = 50000, fill = "", locked = False):
        self.ID=ID
        self.pos=pos
        self.r=r
        self.v=v
        self.m=m
        self.fill = fill
        self.locked=locked
    def moveto(self, pos):
        self.pos=pos
    def move(self):
        self.pos += self.v

class Timer():
    # 计时器
    def __init__(self, root, func, time, enabled):
        self.rt = root
        self.func = func
        self.t=int(time)
        self.enabled=enabled
        if enabled:
            self.enable()
    def timeup(self):
        self.func()
        self.ti = self.rt.after(self.t, self.timeup)
    def enable(self):
        self.enabled = True
        self.timeup()
    def unable(self):
        self.enabled = False
        self.rt.after_cancel(self.ti)
    def reset_time(self, t):
        self.unable()
        self.t=int(t)
        self.enable()

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

Balls = []
id_pool = ID_Pool()
FPS = 60
DeadTime = 1e9
CountNum = 0

def draw_ball(ball):
    if ball.fill != "":
        cv.create_oval(ball.pos.x - ball.r, ball.pos.y - ball.r, ball.pos.x + ball.r, ball.pos.y + ball.r, fill = ball.fill)
    else:
        cv.create_oval(ball.pos.x - ball.r, ball.pos.y - ball.r, ball.pos.x + ball.r, ball.pos.y + ball.r)

def creat_ball(p, r=3, v=Vel(0,0), m=500, fill = "", locked = False):
    ball_t = Ball(id_pool.getid(), p, r, v, m, fill, locked)
    Balls.append(ball_t)
    draw_ball(ball_t)

def del_ball(ball):
    Balls.remove(ball)

def update(cv):
    #更新整个画布
    cv.delete("all")
    for ball in Balls:
        draw_ball(ball)

def solvefunc(a, b, c):
    delta = math.sqrt(b*b-4*a*c)
    return [(-b+delta)/(2*a), (-b-delta)/(2*a)]

def force(b1, b2):
    plus = -1
    x = b1.pos.x - b2.pos.x
    y = b1.pos.y - b2.pos.y
    dis = x*x + y*y
    if dis == 0:
        return
    if math.sqrt(dis) < b1.r + b2.r :
        plus = (b1.r + b2.r) / math.sqrt(dis)
        dis = (b1.r + b2.r) ** 2
    f = 0.05 * b1.m * b2.m / dis
    fx = f / math.sqrt(dis) * x
    fy = f / math.sqrt(dis) * y
    return Vect(fx * plus, fy * plus)

def hit(b1, b2):
    # 碰撞计算
    global CountNum
    CountNum += 100
    dv = b1.v-b2.v
    if dv.mod()==0:
        return
    if hited(b1,b2) == False:
        return
    dp = b2.pos-b1.pos
    dt=0
    if dp.mod() < b1.r+b2.r:
        #print("dis = ", dp.mod(), "dv=", dv.x,",",dv.y)
        a = dv.x**2 + dv.y**2
        b = -2 * (dv.x * dp.x + dv.y * dp.y)
        c = dp.x**2 + dp.y**2 - (b1.r+b2.r) **2
        dt = solvefunc(a, b, c)[1]
        b1.pos += dt * b1.v
        b2.pos += dt * b2.v
        #print("dt=", dt)
    # 球恢复到“碰撞瞬间”
    
    b1.v-=b2.v
    dp = b2.pos-b1.pos
    alpha = 0
    
    #print("now dis = ", dp.mod(), "dv=", dv.x,",",dv.y)
    if dp.x == 0:
        if dp.y > 0:
            alpha = math.asin(1)
        else:
            alpha = math.asin(-1)
    else:
        alpha = math.atan(dp.y/dp.x)
    v0 = b1.v * Vel(math.cos(alpha), math.sin(alpha))
    v0c = b1.v - (v0 * Vel(math.cos(alpha), math.sin(alpha)))
    #print("v0=" , v0, "vel=", Vel(math.cos(alpha), math.sin(alpha)).x, Vel(math.cos(alpha), math.sin(alpha)).y)
    b1.v=b2.v
    b2.v += float((2*b1.m)/(b1.m+b2.m)) * (v0 * Vel(math.cos(alpha), math.sin(alpha)))
    b1.v += float((b1.m-b2.m)/(b1.m+b2.m)) * (v0 * Vel(math.cos(alpha), math.sin(alpha))) + v0c
    # 球弹开
    dt = -dt
    b1.pos += dt * b1.v
    b2.pos += dt * b2.v

    #弹性系数
    #b1.v=b1.v*0.9
    #b2.v=b2.v*0.9

def hited(b1, b2):
    # 是否碰撞
    return (b1.v-b2.v).mod() != 0 and dis(b1.pos, b2.pos) <= b1.r + b2.r - 0.00001

def count_hit():
    global CountNum
    stp = len(Balls)
    hits = []
    for i in range(0, stp - 1):
        for j in range(i + 1, stp):
            CountNum += 2
            if hited(Balls[i], Balls[j]):
                hits.append(Pair(Balls[i].r + Balls[j].r - dis(Balls[i].pos, Balls[j].pos), [Balls[i], Balls[j]]))
    hits.sort()
    #if len(hits):
    #    print(str(len(hits)))
    return hits

def dis(p1, p2):
    return (p1-p2).mod()

def move():
    # 初次计算
    energy=0
    for ball in Balls:
        energy+=ball.v*ball.v*ball.m
        global CountNum
        CountNum += 1
        # ball.v.y+=1
        ball.move()
        if ball.pos.x <= 0:
            ball.v.x *= -1
            ball.pos.x = 1
        if ball.pos.x >= WIDTH:
            ball.v.x *= -1
            ball.pos.x = WIDTH - 1
        if ball.pos.y <= 0:
            ball.v.y *= -1
            ball.pos.y = 1
        if ball.pos.y >= HEIGHT:
            ball.v.y *= -1
            ball.pos.y = HEIGHT - 1
    #print(energy)
def main_loop():
    # 主循环
    global CountNum
    CountNum = 0
    move()
    while CountNum < DeadTime:
        hitlist = count_hit()
        if len(hitlist) == 0:
            break
        for hits in hitlist:
            hit((hits.y)[0], (hits.y)[1])
    for ball in Balls:
        for oth in Balls:
            if ball.ID != oth.ID:
                ball.v += 1/ball.m * force(ball, oth)
    update(cv)

def mouse_press(event):
    global mouseball
    mouseball = creat_ball(Pos(event.x,event.y), 20, Vel(0,0), 50000,  fill = "yellow")

def mouse_up(event):
    global mouseball
    del_ball(mouseball)

def cmd_click():
    if timer.enabled:
        timer.unable()
    else:
        timer.enable()

WIDTH = 500
HEIGHT = 500

root = tk.Tk()                 
root.title("Test")
root.geometry('630x520')

timer = Timer(root, main_loop, 1000/FPS, False)

cv = tk.Canvas(root, bg='skyblue', height=HEIGHT, width=WIDTH)
cmd = tk.Button(root, text="Start move!", width=int(100/7), height=int(20/17), command=cmd_click)
#tst = tk.Button(root, text="Kill Velocity", width=15, height=2, command=stopall)

#for i in [60*x for x in range(1,2)]:
#    for j in [60*x for x in range(int(i/60),9)]:
#        creat_ball(Pos(i,j), 20, Vel(0,0), fill = "red")
# creat_ball(Pos(200,230), 20, Vel(0,6), 500000, fill = "blue")
# creat_ball(Pos(300,270), 20, Vel(0,-6), 5000,  fill = "red")

cv.bind("<ButtonRelease-1>", mouse_press)
cv.bind("<Double-Button-1>", mouse_up)



cv.place(x=5, y=5)
cmd.place(x=505 + 10, y=5)
#tst.place(x=505 + 10, y=55)

root.mainloop()
