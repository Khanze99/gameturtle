import math
import time
import turtle
import random
import os

window = turtle.Screen()
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
pict_path = os.path.join(BASE_PATH, "image", "background.png")


ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300
BASE_ravel_x, BASE_ravel_y = random.randint(-400, 400), 300

enemy_missiles = []
our_missiles = []


BUILDINGS_INFOs = {
    'house': [BASE_X - 400, BASE_Y],
    'kremlin': [BASE_X - 200, BASE_Y],
    'nuclear': [BASE_X + 200, BASE_Y],
    'skyscraper': [BASE_X + 400, BASE_Y] }


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

    INITIAL_HEALTH = 1000

    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y

        self.health = self.INITIAL_HEALTH
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

        text_health = turtle.Turtle(visible=False)
        text_health.speed(0)
        text_health.penup()
        text_health.color("purple")
        text_health.setpos(x=self.x, y=self.y - 65)
        text_health.write(str(self.health), align="center", font=["Arial", 10, "bold"])
        self.text_health = text_health
        self.label_health = self.health


    def get_pic_name(self):
        if self.health  < self.INITIAL_HEALTH * 0.2:
            return f"{self.name}_3.gif"
        elif self.health < self.INITIAL_HEALTH * 0.5:
            return f"{self.name}_2.gif"
        return f"{self.name}_1.gif"


    def draw(self):
        pic_name = self.get_pic_name()
        pic_path = os.path.join(BASE_PATH, "image", pic_name)
        if self.pen.shape() != pic_path:
            window.register_shape(pic_path)
            self.pen.shape(pic_path)
        if self.health != self.label_health:
            self.label_health = self.health
            self.text_health.clear()
            self.text_health.write(str(self.label_health), align="center", font=["Arial", 10, "bold"])
        if self.health < 0:
            self.text_health.clear()




    def is_alive(self):
        return self.health >= 0


class Missile_Base(Building):
    INITIAL_HEALTH = 2000

    def get_pic_name(self):
        for missile in our_missiles:
            if missile.distance(self.x, self.y) < 50:
                pic_name = f"{self.name}_opened.gif"
                break
        else:
            pic_name = f"{self.name}.gif"
        return pic_name


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    alive_buildings = [b for b in buildings if b.is_alive()]
    if alive_buildings:
        target = random.choice(alive_buildings)
        info = Missile(x=x, y=y, color='red', x2=target.x, y2=target.y)
        enemy_missiles.append(info)


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y + 30, x2=x, y2=y)
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


def draw_buildings():
    for building in buildings:
        building.draw()

def game():

    global our_missiles, enemy_missiles, buildings, base

    window.clear()
    window.bgpic(pict_path)
    window.setup(1200 + 3, 800 + 3)
    window.screensize(1200, 800)
    window.tracer(n=6)
    window.onclick(fire_missile)

    buildings = []
    base = Missile_Base(x=BASE_X, y=BASE_Y, name="base")
    buildings.append(base)



    for name, position in BUILDINGS_INFOs.items():
        building = Building(x=position[0], y=position[1], name=name)
        buildings.append(building)



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
            break
        draw_buildings()
        check_impact()
        move_missiles(missiles=our_missiles)
        check_enemy_count()
        check_interceptions()
        move_missiles(missiles=enemy_missiles)
        time.sleep(.01)


    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    pen.color("#9370DB")
    pen.write('GAME OVER', align="center", font=["Arial", 20, "bold"])



while True:
    game()
    answer = window.textinput(title="Hello", prompt="You want play again? Y/N")
    if answer.lower() not in ('y', 'yes', 'д', 'да'):
        break