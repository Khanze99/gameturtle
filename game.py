import math
import turtle
import random
import os


BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
pict_path = os.path.join(BASE_PATH, "image", "background.png")

window = turtle.Screen()
window.bgpic(pict_path)
window.setup(1200 + 3, 800 + 3)
window.screensize(1200, 800)
window.tracer(n=6)

class Missile:

    def __init__(self, x, y, color, x2, y2):
        self.x = x
        self.y = y
        self.color = color
        pen = turtle.Turtle()
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading = pen.towards(x2, y2)
        pen.setheading(heading)
        pen.showturtle()
        self.pen = pen
        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(4)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()


    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300
BASE_ravel_x, BASE_ravel_y = random.randint(-400, 400), 300

enemy_missiles = []
our_missiles = []

# def create_missile(color, x, y, x2, y2):
    # missile = turtle.Turtle()
    # missile.speed(0)
    # missile.color(color)
    # missile.penup()
    # missile.setpos(x=x, y=y)
    # missile.pendown()
    # heading = missile.towards(x2, y2)
    # missile.setheading(heading)
    # missile.showturtle()
    # info = {'missile': missile, 'target': [x2, y2], 'state': 'launched', 'radius': 0}
    # missile = Missile(x=x, y=y, color=color, x2=x2, y2=y2)
    # return missile


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    info = Missile(x=x, y=y, color='red', x2=BASE_X, y2=BASE_Y)
    enemy_missiles.append(info)


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def move_missiles(missiles):
    for missile in missiles:
        missile.step()
        # state = info['state']
        # missile = info['missile']
        # if state == 'launched':
        #     missile.forward(4)
        #     target = info['target']
        #     if missile.distance(x=target[0], y=target[1]) < 20:
        #         info['state'] = 'explode'
        #         missile.shape('circle')
        # elif state == 'explode':
        #     info['radius'] += 1
        #     if info["radius"] > 5:
        #         missile.clear()
        #         missile.hideturtle()
        #         info["state"] = 'dead'
        #     else:
        #         missile.shapesize(info['radius'])
        # elif state == 'dead':
        #     missile.clear()
        #     missile.hideturtle()


    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)

window.onclick(fire_missile)

def check_interceptions():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        # our_missile = our_missile['missile']
        for enemy_missile in enemy_missiles:
            # enemy_missile = enemy_missile['missile']
            if enemy_missile.distance(our_missile.pen.xcor(), our_missile.pen.ycor()) < our_missile.radius*10:
                enemy_missile.state = 'dead'

def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()



base = turtle.Turtle()
base.hideturtle()
base.speed(0)
base.penup()
base.setpos(x=BASE_X, y=BASE_Y)
pic_path = os.path.join(BASE_PATH, "image", "base.gif")
window.register_shape(pic_path)
base.shape(pic_path)
base.showturtle()

base_health = 2000

def game_over():
    return base_health < 0


def check_impact():
    global base_health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        # enemy_missile = enemy_missile.state
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_missile.radius*10:
            base_health -= 100




while True:
    window.update()
    if game_over():
        continue
    check_impact()
    move_missiles(missiles=our_missiles)
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=enemy_missiles)