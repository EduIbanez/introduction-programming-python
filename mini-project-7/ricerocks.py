# RiceRocks

import simpleguitk as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
limit_rocks = 12
safe_distance = 150
velocity_incremented = False
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/images/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/images/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/images/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/images/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/images/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/images/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/images/explosion_alpha.png")

# sound assets purchased
soundtrack = simplegui.load_sound("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/audio/soundtrack.ogg")
missile_sound = simplegui.load_sound("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/audio/missile.ogg")
missile_sound.set_volume(0.5)
ship_thrust_sound = simplegui.load_sound("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/audio/thrust.ogg")
explosion_sound = simplegui.load_sound("https://raw.githubusercontent.com/EduIbanez/introduction-programming-python/master/mini-project-7/audio/explosion.ogg")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        offset = 0
        if self.thrust:
            offset = self.image_size[0]
        canvas.draw_image(self.image, [self.image_center[0] + offset, self.image_center[1]], self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # Angle update
        self.angle += self.angle_vel
        
        # Position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Thrust update
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += (forward[0] * 0.4)
            self.vel[1] += (forward[1] * 0.4)
        
        # Friction update
        self.vel[0] *= (1 - 0.1)
        self.vel[1] *= (1 - 0.1)

    def set_angle_vel(self, rotation):
        self.angle_vel = rotation
    
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        velocity = [self.vel[0] + (forward[0] * 6), self.vel[1] + (forward[1] * 6)]
        a_missile = Sprite([self.pos[0] + (self.radius * forward[0]), self.pos[1] +(self.radius * forward[1])], velocity,
                           self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    def increment_velocity(self):
        self.vel[0] *= 1.4
        self.vel[1] *= 1.4
    
    def draw(self, canvas):
        if self.animated:
            center = [self.image_center[0] + (self.image_size[0] * self.age), self.image_center[1]]
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True
    
    def collide(self, other_object):
        distance = dist(self.pos, other_object.get_position())
        if distance < (self.radius + other_object.get_radius()):
            return True
        else:
            return False

def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.set_angle_vel(-0.15)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.set_angle_vel(0.15)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    if (key == simplegui.KEY_MAP["left"]):
        my_ship.set_angle_vel(0)
    elif (key == simplegui.KEY_MAP["right"]):
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    lives = 3
    score = 0
    soundtrack.rewind()
    soundtrack.play()
    if (not started) and inwidth and inheight:
        started = True

def draw(canvas):
    global time, lives, score, started, velocity_incremented
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw and update ship
    my_ship.draw(canvas)
    my_ship.update()
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    process_sprite_group(missile_group, canvas)
    
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    score += group_group_collide(rock_group, missile_group)
    
    if (score % 30) >= 29:
        if not velocity_incremented:
            for sprite in set(rock_group):
                sprite.increment_velocity()
            velocity_incremented = True
    else:
        velocity_incremented = False
    
    if lives <= 0:
        started = False
        for sprite in set(rock_group):
            rock_group.discard(sprite)
        soundtrack.pause()
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) <= limit_rocks and started:
        distance = 0
        while distance < safe_distance:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            distance = dist(my_ship.get_position(), rock_pos)
        rock_vel = [random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3]
        rock_ang_vel = random.random() * 0.2 - 0.1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)

def process_sprite_group(sprite_set, canvas):
    for sprite in set(sprite_set):
        sprite.draw(canvas)
        if sprite.update():
            sprite_set.discard(sprite)

def group_collide(group, other_object):
    global explosion_group
    collision = False
    for sprite in set(group):
        if sprite.collide(other_object):
            a_explosion = Sprite(sprite.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(a_explosion)
            group.discard(sprite)
            collision = True
    return collision

def group_group_collide(first_group, second_group):
    num_collisions = 0
    for sprite in set(first_group):
        collision = group_collide(second_group, sprite)
        if collision:
            first_group.discard(sprite)
            num_collisions += 1
    return num_collisions

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
explosion_group = set([])
missile_group = set([])

# register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
