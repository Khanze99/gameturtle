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

ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300
BASE_ravel_x, BASE_ravel_y = random.randint(-400, 400), 300

enemy_missiles = []
our_missiles = []

def create_missile(color, x, y, x2, y2):
    missile = turtle.Turtle()
    missile.speed(0)
    missile.color(color)
    missile.penup()
    missile.setpos(x=x, y=y)
    missile.pendown()
    heading = missile.towards(x2, y2)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [x2, y2], 'state': 'launched', 'radius': 0}
    return info


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    info = create_missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
    enemy_missiles.append(info)


def fire_missile(x, y):
    info = create_missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def move_missiles(missiles):
    for info in missiles:
        state = info['state']
        missile = info['missile']
        if state == 'launched':
            missile.forward(4)
            target = info['target']
            if missile.distance(x=target[0], y=target[1]) < 20:
                info['state'] = 'explode'
                missile.shape('circle')
        elif state == 'explode':
            info['radius'] += 1
            if info["radius"] > 5:
                missile.clear()
                missile.hideturtle()
                info["state"] = 'dead'
            else:
                missile.shapesize(info['radius'])
        elif state == 'dead':
            missile.clear()
            missile.hideturtle()


    dead_missiles = [info for info in missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)

window.onclick(fire_missile)

def check_interceptions():
    for our_info in our_missiles:
        if our_info['state'] != 'explode':
            continue
        our_missile = our_info['missile']
        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info['missile']
            if enemy_missile.distance(our_missile.xcor(), our_missile.ycor()) < our_info['radius']*10:
                enemy_info['state'] = 'dead'

def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


while True:
    window.update()
    move_missiles(missiles=our_missiles)
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=enemy_missiles)