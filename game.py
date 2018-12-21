import math
import turtle
import random
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
pict_path = os.path.join(BASE_PATH, "image", "background.png")


ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300
BASE_ravel_x, BASE_ravel_y = random.randint(-400, 400), 300

enemy_missiles = []
our_missiles = []

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
    @property
    def get_x(self):
        return self.pen.xcor()
    @property
    def get_y(self):
        return self.pen.ycor()


class Building:

    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y


        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        pen.penup()
        pen.setpos(x=self.x, y=self.y)
        pic_path = os.path.join(BASE_PATH, "image", self.get_pic_name())
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()
        self.pen = pen
        self.health = 2000


    def get_pic_name(self):

        return f"{self.name}_1.gif"



class Missile_Base(Building):
    def get_pic_name(self):
        return f"{self.name}.gif"


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    target = random.choice(buildings)
    info = Missile(x=x, y=y, color='red', x2=target.x, y2=target.y)
    enemy_missiles.append(info)


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def move_missiles(missiles):
    for missile in missiles:
        missile.step()


    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)



def check_interceptions():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius*10:
                enemy_missile.state = 'dead'

def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()






window = turtle.Screen()
window.bgpic(pict_path)
window.setup(1200 + 3, 800 + 3)
window.screensize(1200, 800)
window.tracer(n=6)
window.onclick(fire_missile)

buildings = []
base = Missile_Base(x=BASE_X, y=BASE_Y, name="base")
buildings.append(base)
buiding_infos = {
    'house': [BASE_X - 400, BASE_Y],
    'kremlin': [BASE_X - 200, BASE_Y],
    'nuclear': [BASE_X + 200, BASE_Y],
    'skyscraper': [BASE_X + 400, BASE_Y] }


for name, position in buiding_infos.items():
    base = Building(x=position[0], y=position[1], name=name)
    buildings.append(base)



def game_over():
    return base.health < 0


def check_impact():
    base.health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        for building in buildings:
            if enemy_missile.distance(building.x, building.y) < enemy_missile.radius*10:
                building.health -= 25
                print(f"{building.name} - {building.health}")




while True:
    window.update()
    if game_over():
        continue
    check_impact()
    move_missiles(missiles=our_missiles)
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=enemy_missiles)