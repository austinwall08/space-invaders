import pygame
import math
import random

pygame.init()

window = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

# region of variables
global start_pos_x
global start_pos_y
start_pos_x = int(pygame.Surface.get_width(window) /2)
start_pos_y = int(pygame.Surface.get_height(window) /2)

shaft_width = 10
shaft_height = 40

ball_size = 8

global accel
accel = 0

global velocity_x
velocity_x = 0
global velocity_y
velocity_y = 0

tip_height = (shaft_height / 2)

global player_surface_x
global player_surface_y
global player_surface

player_surface_x = 35
player_surface_y = 55
player_surface = pygame.Surface((player_surface_x, player_surface_y), pygame.SRCALPHA)

global angle
angle = 0

global fuel
fuel = 100

global accel_x
accel_x = 0
global accel_y
accel_y = 0

global game_begin
game_begin = False

global score
score = 0
# endregion

def draw_player():
            
        #region of variables for player
        center_x = player_surface_x/2
        center_y = player_surface_y/7.5
        left_shaft_start = center_x - (shaft_width/2)
        shaft_top = center_y

        ball1_center_x = center_x - ball_size
        ball1_center_y = center_y + shaft_height
        ball2_center_x = center_x + ball_size
        ball2_center_y = center_y + shaft_height

        tip_left = center_x - shaft_width/1.25
        tip_top = center_y - shaft_height / 4.5
        tip_width =  (shaft_width + 20)/1.75

       
        # endregion

        player_surface.fill((0, 0, 0, 0))

        shaft = (pygame.draw.rect
                            (player_surface, 
                             "tan", 
                             pygame.Rect(left_shaft_start, shaft_top, shaft_width, shaft_height),
                               ),
            
                pygame.draw.rect
                            (player_surface, 
                             "black", 
                             pygame.Rect(left_shaft_start, shaft_top, shaft_width, shaft_height),
                               1))

        ball1 = (pygame.draw.circle
                        (player_surface, 
                        "tan", 
                        (ball1_center_x,
                            ball1_center_y), 
                        ball_size),  
                    
                pygame.draw.circle
                        (player_surface, 
                            "black", 
                        (ball1_center_x, 
                            ball1_center_y), 
                        ball_size, 
                        1))
        
        ball2 = (pygame.draw.circle
                        (player_surface, 
                        "tan", 
                        (ball2_center_x, 
                        ball2_center_y), 
                        ball_size),  
                    
                pygame.draw.circle
                        (player_surface, 
                            "black", 
                        (ball2_center_x, 
                        ball2_center_y), 
                        ball_size, 
                        1))
                
        tip =   (pygame.draw.arc
                    (player_surface, 
                    "pink", 
                    pygame.Rect(tip_left, tip_top, tip_width, tip_height), 
                    start_angle = 0, 
                    stop_angle = 3.14, 
                    width = 100), 
                
                pygame.draw.arc
                        (player_surface, 
                        "black", 
                        pygame.Rect(tip_left, tip_top, tip_width, tip_height), 
                        start_angle = 0, 
                        stop_angle = 3.14,))

def rotate_player():
    global angle

    if press_keys[pygame.K_d]:
        angle -= 180 * dt

    if press_keys[pygame.K_a]:
        angle += 180 * dt

    if angle >= 360 or angle <= -360:
        angle = 0

    return pygame.transform.rotate(player_surface, angle)

def boundary(player_rect):

    global velocity_x
    global velocity_y
    global start_pos_x
    global start_pos_y
    collision_rect = pygame.Rect(20, 20, 1240, 680)

    if player_rect.bottom >= collision_rect.bottom:
        start_pos_y -= player_rect.bottom - collision_rect.bottom
        velocity_y *= 0
    elif player_rect.top <= collision_rect.top:
        start_pos_y -= player_rect.top - collision_rect.top
        velocity_y *= 0

    if player_rect.left <= collision_rect.left:
        start_pos_x -= player_rect.left - collision_rect.left
        velocity_x *= 0
    elif player_rect.right >= collision_rect.right:
        start_pos_x -= player_rect.right - collision_rect.right
        velocity_x *= 0

def inertia():
    global velocity_x, velocity_y
    global start_pos_x, start_pos_y
    global fuel
    global accel_x, accel_y
    acceleration = 100

    accel_x = 0
    accel_y = 0
 
    if fuel > 0:
        if press_keys[pygame.K_w]:
            accel_x -= math.sin(math.radians(angle)) * acceleration
            accel_y -= math.cos(math.radians(angle)) * acceleration

        if press_keys[pygame.K_s]:
            accel_x += math.sin(math.radians(angle)) * acceleration
            accel_y += math.cos(math.radians(angle)) * acceleration 

    velocity_x += accel_x * dt
    velocity_y += accel_y * dt

    start_pos_x += velocity_x * dt
    start_pos_y += velocity_y * dt
    draw_player()

def reset_game():
    global start_pos_x, start_pos_y, angle, velocity_x, velocity_y, spawn_time, fuel, score

    enemies.clear()
    bullets.clear()
    start_pos_x = int(pygame.Surface.get_width(window) /2)
    start_pos_y = int(pygame.Surface.get_height(window) /2)
    angle = 0
    velocity_x = 0
    velocity_y = 0
    spawn_time = 0
    fuel = 100
    score = 0

def fuel_system():
    global fuel, accel_x, accel_y

    if fuel <= 0:
        fuel = 0
        fuel_out_font = pygame.font.SysFont("stencil", 35)
        fuel_out_text_surface = fuel_out_font.render("FUEL IS OUT, SHOOT ASTEROIDS TO GET MORE", True, ("Red"))
        window.blit(fuel_out_text_surface, (1280/4.5, 720/2))
    elif accel_x != 0 or accel_y != 0:
        fuel -= 10 * dt
    fuel_font = pygame.font.SysFont("segoeuisemilight", 35)
    fuel_text_surface = fuel_font.render(f"Fuel: {int(fuel)}", True, (255, 255, 255))
    window.blit(fuel_text_surface, (1100, 620))

    return fuel

def start_screen():

    start_font = pygame.font.SysFont("corbel", 80)
    control_font = pygame.font.SysFont("corbel", 25)
    control_display_font = pygame.font.SysFont("corbel", 50)
    start_game_font = pygame.font.SysFont("corbel", 15)

    start_screen = pygame.Surface((1280, 720))
    start_screen.fill("White")

    line1 = start_font.render("Welcome to Spenis Invaders", True, (255, 255, 255))
    line2 = control_display_font.render("Controls:", True, (255, 255, 255))
    line3 = control_font.render("W/S to move, A/D to Turn", True, (255, 255, 255))
    line4 = control_font.render("Space to Shoot", True, (255, 255, 255))
    line5 = control_font.render("ESC to Pause", True, (255, 255, 255))
    line6 = control_font.render("Good Luck!", True, (255, 255, 255))
    line7 = start_game_font.render("(G to Start)", True, (255, 255, 255))
    line8 = start_game_font.render("(F to Toggle Full Screen)", True, (255, 255, 255))

    window.blit(line1, (225, 100))
    window.blit(line2, (550, 200))
    window.blit(line3, (525, 280))
    window.blit(line4, (575, 360))
    window.blit(line5, (580, 440))
    window.blit(line6, (595, 540))
    window.blit(line7, (620, 600))
    window.blit(line8, (590, 640))

def display_score():
    global score

    score_font = pygame.font.SysFont("Corbel", 50)
    score_display = score_font.render(f"Score: {int(score)}", True, (255, 255, 255))
    window.blit(score_display, (375, 25))

def display_max_score():
    global score

    scores.append(score)

    max_score = max(scores)
    max_score_font = pygame.font.SysFont("Corbel", 50)
    max_score_display = max_score_font.render(f"Max Score: {int(max_score)}", True, (255, 255, 255))
    window.blit(max_score_display, (600, 25))

class Enemy:

    def __init__(self, center_x, center_y, radius, durability, score_amount):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius 
        self.durability = durability
        self.score_amount = score_amount

        self.enemy_speed = 100
        self.angle = random.randint(0, 360)
        self.velocity_x = math.sin(math.radians(self.angle)) * self.enemy_speed
        self.velocity_y = math.cos(math.radians(self.angle)) * self.enemy_speed
        
    def spawn_enemy(self):
       pygame.draw.circle(window, (64, 64, 64), (self.center_x, self.center_y), self.radius)

    def move_enemy(self):
        self.center_x += self.velocity_x * dt
        self.center_y += self.velocity_y * dt


    def boundary(self):
        if (self.center_x - self.radius) <= -100 and self.velocity_x < 0:
            self.center_x = -100 + self.radius
            if self.velocity_x < 0:
                self.velocity_x *= -1
        elif (self.center_x + self.radius) >= 1380 and self.velocity_x > 0:
            self.center_x = 1380 - self.radius
            if self.velocity_x > 0:
                self.velocity_x *= -1

        if (self.center_y - self.radius) <= -100 and self.velocity_y < 0:
            self.center_y = -100 + self.radius
            if self.velocity_y < 0:
                self.velocity_y *= -1
        elif (self.center_y + self.radius) >= 820 and self.velocity_y > 0:
            self.center_y = 820 - self.radius
            if self.velocity_y > 0:
                self.velocity_y *= -1
    
    def enemy_collision(self, enemy):
        distance = math.sqrt((self.center_x - enemy.center_x)**2 + (self.center_y - enemy.center_y)**2)
        if distance <= self.radius + enemy.radius:
            self.velocity_x *= -1
            self.velocity_y *= -1
            enemy.velocity_x *= -1
            enemy.velocity_y *= -1
    
    def colliding_with_player(self):
        closest_x = max(player_rect.left, min(self.center_x, player_rect.right))

        closest_y = max(player_rect.top, min(self.center_y, player_rect.bottom))

        distance_x = self.center_x - closest_x
        distance_y = self.center_y - closest_y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        if distance <= self.radius:
            return True
        else: return False

    def take_damage(self, bullet):
        global fuel
        global score

        self.durability -= bullet.damage
        if self.durability <= 0:
            fuel += self.radius
            score += self.radius
            enemies.remove(enemy)

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.bullet_speed = 500
        self.velocity_x = 0
        self.velocity_y = 0
        self.radius = 2.5
        self.damage = 5
      

    def spawn_bullet(self):
        pygame.draw.circle(window, "white", (self.x, self.y), self.radius)

    def move_bullet(self):

        self.velocity_x = -math.sin(math.radians(self.angle)) * self.bullet_speed
        self.velocity_y = -math.cos(math.radians(self.angle)) * self.bullet_speed

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt 

    def collide_with_enemy(self, enemy):
        distance = math.sqrt((self.x - enemy.center_x)**2 + (self.y - enemy.center_y)**2)

        if distance <= self.radius + enemy.radius:
            return True
        else: return False

    def leave_boundary(self):
        if self.x >= 1282.5 or self.x <= -2.5:
            if bullet in bullets:
                bullets.remove(self)
        if self.y >= 722.5 or self.y <= -2.5:
            if bullet in bullets:
                bullets.remove(self)

class Stars:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.radius = 2

    def draw_stars(self):
        pygame.draw.circle(window, "white", (self.x, self.y), self.radius)

global game_paused
game_paused = False

global game_lost
game_lost = False

scores = [0]
enemies = []
bullets = []
stars = []

global spawn_time
spawn_time = 0

while running is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused
            elif event.key == pygame.K_SPACE and not game_paused and len(bullets) < 10:
                bullets.append(Bullet(start_pos_x, start_pos_y, angle))

            if event.key == pygame.K_g:
                game_begin = True

            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    dt = clock.tick(60) / 1000
    window.fill("black")

    if game_begin == False:
        start_screen()

    if game_begin == True:
        if len(stars) < 50:
            stars.append(Stars(random.randrange(0, 1280), random.randrange(0, 720)))

        for star in stars:
            star.draw_stars()

        if game_lost == False:

            if game_paused == False:

                random_score_amount = random.randrange(5, 21)

                spawn_time += dt

                if len(enemies) < 20 and spawn_time > .5:
                    enemies.append(Enemy(random.randrange(40, 1280), random.randrange(-75, 805, 820), random_score_amount, random_score_amount, random_score_amount))
                    spawn_time = 0

                display_score()

                display_max_score()

                press_keys = pygame.key.get_pressed()

                rotated_surface = rotate_player()

                inertia()

                player_rect = rotated_surface.get_rect(center=(start_pos_x, start_pos_y))
                window.blit(rotated_surface, player_rect)
                
                boundary(player_rect)

                for bullet in bullets:
                    bullet.move_bullet()
                    bullet.spawn_bullet()
                    bullet.leave_boundary()
                    for enemy in enemies:
                        if bullet.collide_with_enemy(enemy) == True:
                            enemy.take_damage(bullet)
                            if bullet in bullets:
                                bullets.remove(bullet)
                                
                for enemy in enemies:
                    enemy.move_enemy()
                    enemy.boundary()
                    enemy.spawn_enemy()
                    if enemy.colliding_with_player() == True:
                        game_lost = True
                
                for self in range(len(enemies)):
                    for enemy in range(self + 1, len(enemies)):
                        enemies[self].enemy_collision(enemies[enemy])

                fuel_system()

            elif game_paused == True:          
                pause_menu = pygame.Surface((1280, 720), pygame.SRCALPHA)
                grey_trans = (100, 100, 100, 5)
                pause_menu.fill(grey_trans)

                pause_font = pygame.font.SysFont("algerian", 100)
                pause_text_surface = pause_font.render("Game Paused", True, (255, 255, 255))
                pause_text_rect = pause_text_surface.get_rect(center = (1280/2, 720/2))

                pause_menu.blit(pause_text_surface, pause_text_rect)
                window.blit(pause_menu, (0, 0))

        elif game_lost == True:
            game_over = pygame.Surface((1280, 720))
            game_over.fill("red")
            
            scores.append(score)

            font = pygame.font.SysFont("algerian", 100)
            font2 = pygame.font.SysFont("algerian", 30)

            text_surface = font.render("Game Over", True, (255, 255, 255))
            text_surface2 = font2.render("Press Enter To Play Again", True, (255, 255, 255))

            text_rect = text_surface.get_rect(center = (1280/2, 720/2))
            text_rect2 = text_surface2.get_rect(center = (625, 470))

            game_over.blit(text_surface2, text_rect2)
            game_over.blit(text_surface, text_rect)
            window.blit(game_over, (0, 0))

            if pygame.key.get_pressed()[pygame.K_RETURN]:
                game_lost = False
                reset_game()

    pygame.display.flip()

pygame.quit()

