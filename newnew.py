import pygame   , sys, math, random

pygame.init()

old = []

screen = pygame.display.set_mode((1280, 650))

pygame.font.init()

clock = pygame.time.Clock()

time = 0

font = pygame.font.Font(pygame.font.get_default_font(), 20)

global_id = 0

blood_images = [pygame.image.load("graphics/blood3.png"), pygame.image.load("graphics/blood4.png")]

objects = []

class Blood:
    def __init__(self, image, instance, x, y):
        self.image = image
        self.rect = image.get_rect(center=(x, y))
        objects.append(self)
        self.instance = instance
        instance.objects.append(self)
        self.time = 1000
class Enemy:
    def __init__(self, hp, x, y, left, right, instance, move_speed, dmg, attack_speed, drop, blueprint, obj):
        self.obj = obj
        self.blueprint = blueprint
        self.move_speed = move_speed
        self.hp = hp
        self.max_hp = hp
        self.left = left
        self.right = right
        self.image = left
        self.rect = self.image.get_rect(center = (x, y))
        self.hp_bar = pygame.Rect(self.rect.x, self.rect.height - 20, 50, 8)
        self.hp_bar.center = (self.rect.center[0], self.rect.y - 15)
        objects.append(self)
        self.instance = instance
        self.dmg = dmg
        instance.objects.append(self)
        self.attack_speed = attack_speed
        self.drop = drop
        self.attack_time = 0
class Weapon:
    def __init__(self, bullet_speed, fpb, image, blueprint, instance, ground, dmg, x, y, name):
        self.name = name
        self.image = image
        self.instance = instance
        self.ground = ground
        self.rect = self.image.get_rect(center=(x, y))
        self.blueprint = blueprint
        self.bullet_speed = bullet_speed
        self.max_fpb = fpb
        self.fpb = 0
        self.dmg = dmg
        objects.append(self)
        instance.objects.append(self)
        self.despawn_time = 1200

class Cursor:
    def __init__(self):
        self.image = pygame.image.load("graphics/cursor.png")
        self.rect = self.image.get_rect()

class Instance:
    def __init__(self, size, floor, wall, difficulty):
        global global_id
        self.objects = []
        self.wall = wall
        self.floor = floor
        self.difficulty = difficulty
        x = 0
        y = 0
        for i in range(size * 13):
            globals()[f"Object{global_id}"] = Tile(x, y, floor if y < 500 else wall, self)
            if i == 0:
                self.start = eval(f"Object{global_id}")
            global_id += 1
            y += 50
            if y == 650:
                y = 0
                x += 50
        objects.append(self)
class Tile:
    def __init__(self, x, y, color, instance):
        self.instance = instance
        self.rect = pygame.Rect(x, y, 50, 50)
        objects.append(self)
        self.color = color
        self.instance.objects.append(self)
class Player:
    def __init__(self):
        self.image = pygame.image.load("graphics/player.png")
        self.instance = world
        self.rect = self.image.get_rect(center=(650, 475))
        self.inventory = []
        self.weapon = pistol1
        self.max_hp = 150
        self.hp = 150
class Wave:
    def __init__(self, num, enemies, time, end):
        self.num = num
        self.enemies = enemies
        self.time = time
        self.time_left = time
        self.end = end
        self.done = False
        objects.append(self)
class Health:
    def __init__(self, health, image, blueprint, instance, x, y):
        self.health = health
        self.image = image
        self.instance = instance
        self.rect = self.image.get_rect(center=(x, y))
        self.blueprint = blueprint
        self.despawn_time = 1200
        objects.append(self)
        self.instance.objects.append(self)
def GetNextWave(current_wave):
    current_wave.done = True
    for x in objects:
        if x.__class__ == Wave and x.num == current_wave.num + 1:
            for y in objects:
                if y.__class__ == Enemy and not y.blueprint:
                    return current_wave
            return x
    return current_wave
class Main:
    def Draw_Instance(instance):
        for self in instance.objects:
            if self.__class__ == Tile:
                if self.color == instance.floor:
                    pygame.draw.rect(screen, self.color, self.rect)
        for self in instance.objects:
            if self.__class__ == Blood:
                screen.blit(self.image, (self.rect.center))
            if self.__class__ == Health:
                if not self.blueprint:
                    screen.blit(self.image, (self.rect.x, self.rect.y))
        for self in instance.objects:
            if self.__class__ == Weapon:
                if self.ground and not self.blueprint:
                    screen.blit(self.image, (self.rect.x, self.rect.y))
        for self in instance.objects:
            if self.__class__ == Enemy and not self.blueprint:
                screen.blit(self.image, (self.rect.x, self.rect.y))
                pygame.draw.rect(screen, (255, 0, 0), self.hp_bar)
        for self in instance.objects:
            if self.__class__ == Bullet:
                screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(player.image, (player.rect.x, player.rect.y))
        for self in instance.objects:
            if self.__class__ == Tile:
                if self.color == instance.wall:
                    pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(cursor.image, (cursor.rect.x, cursor.rect.y))
    def Move_Bullets():
        for self in objects:
            if self.__class__ == Bullet:
                self.rect.center = calculat_new_xy(self.rect.center, self.speed, self.angle)
                self.kill_time -= 1
                if self.kill_time == 0:
                    objects.remove(self)
                    self.instance.objects.remove(self)
                    old.append(self)
    def Time_Things():
        global time
        global global_id
        global current_wave
        screen.blit(update_fps(), (10,0))
        for self in objects:
            if self.__class__ == Bullet:
                self.kill_time -= 1
                if self.kill_time == 0:
                    objects.remove(self)
                    self.instance.objects.remove(self)
                    old.append(self)
        for self in objects:
            if self.__class__ == Weapon:
                if self.fpb > 0:
                    self.fpb -= 1
                if self == player.weapon:
                    self.despawn_time = 600
                else:
                    self.despawn_time -= 1
                    if self.despawn_time < 1:
                        objects.remove(self)
                        self.instance.objects.remove(self)
                if self.rect.y < 450:
                    self.rect.y += 1
            if self.__class__ == Health:
                self.despawn_time -= 1
                if self.despawn_time < 1:
                    objects.remove(self)
                    self.instance.objects.remove(self)
        for self in objects:
            if self.__class__ == Enemy:
                if self.attack_time > 0:
                    self.attack_time -= 1
        for self in objects:
            if self.__class__ == Blood:
                self.time -= 1
                if self.time < 1:
                    objects.remove(self)
                    self.instance.objects.remove(self)
                    old.append(self)
        for x in player.instance.objects:
            if x.__class__ == Health and x.rect.colliderect(player.rect) and not player.hp >= player.max_hp:
                objects.remove(x)
                x.instance.objects.remove(x)
                player.hp += x.health
                if player.hp > player.max_hp: player.hp = player.max_hp
        player_hp_text = font.render(f"Hp: {player.hp} / {player.max_hp}", True, (255, 0, 0))
        screen.blit(player_hp_text, (50, 50))
        time_text = font.render(f"Time: {time}", True, (255, 255, 255))
        screen.blit(time_text, (50, 525))
        weapon_name_text = font.render(f"Weapon: {'None' if player.weapon == None else player.weapon.name}", True, (255, 255, 255))
        screen.blit(weapon_name_text, (700, 50))
        wave_time_text = font.render(f"Current Wave: {current_wave.num}     Time Left: {current_wave.time_left}", True, (255, 255, 255))
        screen.blit(wave_time_text, (700, 100))
        time += 1
        if current_wave.time_left < 1:
            if current_wave.done == False:
                for x in current_wave.end:
                    for i in range(x[1]):
                        local_enemy = x[0]
                        globals()[f"Objects{global_id}"] = Enemy(local_enemy.hp, 200 if random.randint(1, 2) == 1 else 1200, 475, local_enemy.left, local_enemy.right, player.instance, local_enemy.move_speed, local_enemy.dmg, local_enemy.attack_speed, local_enemy.drop, False, local_enemy)
                        global_id += 1
            current_wave = GetNextWave(current_wave)
        if current_wave.done == False:
            current_wave.time_left -= 1
        if player.hp <= 0:
            print(time)
            pygame.quit()
            sys.exit()
        if current_wave.done == False:
            if random.randint(1, 245) == 1:
                ra = random.randint(1, 100)
                for x in current_wave.enemies:
                    if ra >= x[1] and ra <= x[2]:
                        local_enemy = x[0]
                        globals()[f"Objects{global_id}"] = Enemy(local_enemy.hp, 200 if random.randint(1, 2) == 1 else 1200, 475, local_enemy.left, local_enemy.right, player.instance, local_enemy.move_speed, local_enemy.dmg, local_enemy.attack_speed, local_enemy.drop, False, local_enemy)
                        global_id += 1
        
            #difficulty = player.instance.difficulty + random.randint(-2, 2)
            #list = []
            #for enemy in objects:
             #   if enemy.__class__ == Enemy and difficulty in enemy.difficulty and enemy.blueprint:
              #      list.append(enemy)
            #if len(list) > 0:
             #   local_enemy = list[random.randint(0, len(list) - 1)]
              #  globals()[f"Objects{global_id}"] = Enemy(local_enemy.hp, 200 if random.randint(1, 2) == 1 else 1200, 475, local_enemy.left, local_enemy.right, player.instance, local_enemy.move_speed, local_enemy.dmg, local_enemy.attack_speed, local_enemy.drop, local_enemy.difficulty, False, local_enemy)
               # global_id += 1
    def Bullet_Collision():
        global global_id
        for bullet in objects:
            if bullet.__class__ == Bullet:
                for collison in objects:
                    if collison.__class__ == Enemy and bullet.attacker == player and collison.rect.colliderect(bullet.rect) and bullet in player.instance.objects and not collison.blueprint:
                        objects.remove(bullet)
                        bullet.instance.objects.remove(bullet)
                        old.append(bullet)
                        collison.hp -= bullet.dmg
                        temp = round(collison.hp / collison.max_hp * 50)
                        collison.hp_bar.width = temp
                        if random.randint(1, 3) == 1:
                            for i in range(random.randint(2, 4)):
                                if len(old) > 0:
                                    old[0] = Blood(blood_images[random.randint(0, len(blood_images) - 1)], player.instance, collison.rect.x + random.randint(-50, 50), collison.rect.y + random.randint(-50, 50))
                                    old.pop(0)
                                else:
                                    globals()[f"Objects{global_id}"] = Blood(blood_images[random.randint(0, len(blood_images) - 1)], player.instance, collison.rect.x + random.randint(-50, 50), collison.rect.y + random.randint(-50, 50))
                                    global_id += 1
                        if collison.hp <= 0:
                            objects.remove(collison)
                            collison.instance.objects.remove(collison)
                            old.append(collison)
                            for x in collison.drop:
                                if random.randint(1, 100) <= x[1]:
                                    if x[0].__class__ == Weapon:
                                        globals()[f"Object{global_id}"] = Weapon(x[0].bullet_speed, x[0].max_fpb, x[0].image, False, player.instance, True, x[0].dmg, collison.rect.x, collison.rect.y, x[0].name)
                                    elif x[0].__class__ == Health:
                                        globals()[f"Object{global_id}"] = Health(x[0].health, x[0].image, False, x[0].instance, collison.rect.x, collison.rect.y)
                                    global_id += 1
                                    break
                    elif collison == player and not bullet.attacker == player and collison.rect.colliderect(bullet.rect) and bullet in player.instance.objects:
                        objects.remove(bullet)
                        bullet.instance.objects.remove(bullet)
                        old.append(bullet)
                        collison.hp -= bullet.dmg
    def Enemy_ai(self):
        global global_id
        if self.__class__ == Enemy:
            if self.rect.colliderect(player.rect) == False:
                if self.rect.x > player.rect.x:
                    self.rect.x -= self.move_speed
                    self.hp_bar.x -= self.move_speed
                    self.image = self.left
                else:
                    self.rect.x += self.move_speed
                    self.hp_bar.x += self.move_speed
                    self.image = self.right
            elif self.rect.colliderect(player.rect):
                if self.attack_time == 0:
                    player.hp -= self.dmg
                    self.attack_time = self.attack_speed
            else:
                self.rect.y = 175
                self.hp_bar.y = 175
class Bullet:
    def __init__(self, angle, speed, pos, instance, image, dmg, attacker):
        self.attacker = attacker
        self.dmg = dmg
        self.image = image
        self.angle = angle
        self.speed = speed
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))
        objects.append(self)
        self.instance = instance
        instance.objects.append(self)
        self.kill_time = 475
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text
move_speed = 3

world = Instance(45, (92, 27, 7), (150, 100, 50), 2)

pistol1 = Weapon(30, 35, pygame.image.load("graphics/pistol.png"), False, world, False, 4, 250, 475, "Pistol")

pistol = Weapon(30, 35, pygame.image.load("graphics/pistol.png"), True, world, True, 4, 250, 475, "Pistol")
rifle = Weapon(40, 20, pygame.image.load("graphics/rifle.png"), True, world, True, 5, 275, 475, "Rifle")
sniper = Weapon(50, 80, pygame.image.load("graphics/sniper.png"), True, world, True, 20, 450, 475, "Sniper Rifle")
mini_gun = Weapon(40, 10, pygame.image.load("graphics/mini.png"), True, world, True, 3, 100, 100, "Mini Gun")

health1 = Health(30, pygame.image.load("graphics/health1.png"), True, world, 0, 0)
health2 = Health(100, pygame.image.load("graphics/health1.png"), True, world, 0, 0)

enemy1 = Enemy(30, 200 if random.randint(1, 2) == 1 else 1200, 475, pygame.image.load("graphics/enemy_left.png"), pygame.image.load("graphics/enemy_right.png"), world, 1, 10, 100, [[sniper, 15], [rifle, 10], [health1, 15]], True, None)
enemy2 = Enemy(15, 200 if random.randint(1, 2) == 1 else 1200, 475, pygame.image.load("graphics/snail_left.png"), pygame.image.load("graphics/snail_right.png"), world, 2, 5, 80, [[pistol, 10], [rifle, 5], [mini_gun, 3], [health1, 15]], True, None)
cow = Enemy(55, 200 if random.randint(1, 2) == 1 else 1200, 475, pygame.image.load("graphics/cow_left.png"), pygame.image.load("graphics/cow_right.png"), world, 1, 10, 100, [[mini_gun, 15], [rifle, 10], [health1, 25]], True, None)
elephant = Enemy(120, 200 if random.randint(1, 2) == 1 else 1200, 475, pygame.image.load("graphics/elephant_left.png"), pygame.image.load("graphics/elephant_right.png"), world, 1, 30, 140, [[pistol, 5], [rifle, 10], [mini_gun, 20], [health1, 100]], True, None)
thing = Enemy(500, 200 if random.randint(1, 2) == 1 else 1200, 475, pygame.image.load("graphics/thing_left.png"), pygame.image.load("graphics/thing_right.png"), world, 1, 40, 140, [[pistol, 5], [rifle, 10], [mini_gun, 40], [health2, 100]], True, None)



wave1 = Wave(1, [[enemy2, 1, 60], [enemy1, 61, 100]], 2400, [])
wave2 = Wave(2, [[enemy2, 1, 40], [enemy1, 41, 85], [cow, 86, 100]], 3000, [])
wave3 = Wave(3, [[enemy2, 1, 40], [enemy1, 41, 80], [cow, 81, 100]], 3000, [[elephant, 1]])
wave4 = Wave(4, [[enemy2, 1, 34], [enemy1, 35, 70], [cow, 71, 95], [elephant, 96, 100]], 4000, [])
wave5 = Wave(5, [[enemy2, 1, 30], [enemy1, 31, 65], [cow, 66, 92], [elephant, 93, 100]], 4000, [])
wave6 = Wave(6, [[enemy2, 1, 20], [enemy1, 21, 40], [cow, 41, 87], [elephant, 88, 100]], 4200, [])

current_wave = wave1

player = Player()

move_xm = False
move_xp = False
button_1 = False

def move_player(xy, plus_minus):
    global global_id
    for x in objects:
        if x.__class__ == Tile or x.__class__ == Weapon or x.__class__ == Enemy or x.__class__ == Blood or x.__class__ == Health:
            if xy == "x" and plus_minus == "plus": 
                x.rect.x += move_speed
                if x.__class__ == Enemy: x.hp_bar.x += move_speed
            if xy == "x" and plus_minus == "minus":
                x.rect.x -= move_speed
                if x.__class__ == Enemy: x.hp_bar.x -= move_speed
    move = False
    for x in objects:
        if x.__class__ == Tile and x.rect.colliderect(player.rect) and x in player.instance.objects:
            move = True
    if not move:
        for x in objects:
            if x.__class__ == Tile or x.__class__ == Weapon or x.__class__ == Enemy or x.__class__ == Blood or x.__class__ == Health:
                if xy == "x" and plus_minus == "plus":
                    x.rect.x -= move_speed
                    if x.__class__ == Enemy: x.hp_bar.x -= move_speed
                if xy == "x" and plus_minus == "minus":
                    x.rect.x += move_speed
                    if x.__class__ == Enemy: x.hp_bar.x += move_speed
def calculat_new_xy(old_xy,speed,angle_in_radians):
    new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
    new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
    return new_x, new_y
pygame.mouse.set_visible(False)

cursor = Cursor()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                move_xm = True
            if event.key == pygame.K_a:
                move_xp = True
            if event.key == pygame.K_e:
                print(len(old))
                drop = True
                for x in objects:
                    if x.__class__ == Weapon and x.rect.colliderect(player.rect) and x in player.instance.objects and x.ground and not x.blueprint:
                        if not player.weapon == None:
                            player.weapon.ground = True
                            player.weapon.rect.center = player.rect.center
                        player.weapon = x
                        x.ground = False
                        drop = False
                        break
                if drop:
                    if not player.weapon == None:
                        player.weapon.ground = True
                        player.weapon.rect.center = player.rect.center
                        player.weapon = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_1 = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_1 = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                move_xm = False
            if event.key == pygame.K_a:
                move_xp = False
    if button_1:
        if not player.weapon == None and player.weapon.fpb == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - player.rect.x, mouse_y - player.rect.y
            angle = math.atan2(rel_y, rel_x)
            if len(old) > 0:
                bullet = old[0] = Bullet(angle, 20, player.rect.center, player.instance, pygame.image.load("graphics/bullet.png"), player.weapon.dmg, player)
                old.pop(0)
            else:
                bullet = globals()[f"Object{global_id}"] = Bullet(angle, 20, player.rect.center, player.instance, pygame.image.load("graphics/bullet.png"), player.weapon.dmg, player)
                global_id += 1
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            bullet.image = pygame.transform.rotozoom(bullet.image, angle, 1)
            player.weapon.fpb = player.weapon.max_fpb
    if move_xm:
        move_player("x", "minus")
    if move_xp:
        move_player("x", "plus")
    screen.fill((0, 255, 0))    

    cursor.rect.center = pygame.mouse.get_pos()

    Main.Draw_Instance(player.instance)
    Main.Move_Bullets()
    Main.Time_Things()
    Main.Bullet_Collision()
    for self in player.instance.objects:
        if self.__class__ == Enemy and not self.blueprint:
            Main.Enemy_ai(self)

    pygame.display.update()

    clock.tick(60)

