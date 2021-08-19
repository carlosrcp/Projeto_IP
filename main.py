import pygame
import os
import random
pygame.font.init()


#? ANCHOR Dimensões e Tela

LARGURA, ALTURA = 600, 1066
TELA = pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption('BRANCH P.17')


#? ANCHOR Importar Assets

##?{

#& Player
SPACE_SHIP_PLAYER = pygame.image.load(os.path.join('assets','spaceship_player.png'))
#&

#& Mobs:
#*{
##! Comuns
COMMON_ENEMY = pygame.image.load(os.path.join('assets','comen1.png'))
COMMON_ENEMY_2 = pygame.image.load(os.path.join('assets','comen2.png'))
##! Comuns

##! Level 1
CAT_6_PURPLE_ENEMY = pygame.image.load(os.path.join('assets','category_6','Ship_colorful_0010_Bitmap------------------.png'))
##!

##! Level 2
CAT_5_PURPLE_ENEMY = pygame.image.load(os.path.join('assets','category_5','specShip_0007_Bitmap------------------.png'))
##!

##! Level 3
CAT_4_PURPLE_ENEMY = pygame.image.load(os.path.join('assets','category_4','ship_neon_0032_Package-----------------.png'))
##!

##! Level 4
CAT_3_PURPLE_ENEMY = pygame.image.load(os.path.join('assets','category_3','ship3_0009_Package-----------------.png'))
CAT_3_TOURM_ENEMY = pygame.image.load(os.path.join('assets','category_3','ship3_0003_Package-----------------.png'))
##!

##! Level 5
CAT_2_CUT_ENEMY = pygame.image.load(os.path.join('assets','category_2','ship2_0002_Package-----------------.png'))
CAT_2_BOWL_ENEMY = pygame.image.load(os.path.join('assets','category_2','ship2_0012_Bitmap------------------.png'))
##!

##! Level 6
CAT_1_DEMIGOD_ENEMY = pygame.image.load(os.path.join('assets','category_1','ship1_0005_Package-----------------.png'))
##!

##! Level 7
GOD_ENEMY = pygame.image.load(os.path.join('assets','category_1','ship1_0001_Package-----------------.png'))
##!
#*}

#& Projectiles:
#*{
##! Roxo
SMALL_LASER_PURPLE = pygame.image.load(os.path.join('assets','04.png'))
GREAT_LASER_PURPLE = pygame.image.load(os.path.join('assets','12.png'))
SMALL_LASER_PURPLE_D = pygame.image.load(os.path.join('assets','04 D.png'))
GREAT_LASER_PURPLE_D = pygame.image.load(os.path.join('assets','12 D.png'))
##!

##! Azul
SMALL_LASER_BLUE = pygame.image.load(os.path.join('assets','01.png'))
GREAT_LASER_BLUE = pygame.image.load(os.path.join('assets','11.png'))
SMALL_LASER_BLUE_D = pygame.image.load(os.path.join('assets','01 D.png'))
GREAT_LASER_BLUE_D = pygame.image.load(os.path.join('assets','11 D.png'))
##!

##! Vermelho
SMALL_LASER_RED = pygame.image.load(os.path.join('assets','02.png'))
GREAT_LASER_RED = pygame.image.load(os.path.join('assets','14.png'))
SMALL_LASER_RED_D = pygame.image.load(os.path.join('assets','02 D.png'))
GREAT_LASER_RED_D = pygame.image.load(os.path.join('assets','14 D.png'))
##!

##! Magenta
SMALL_LASER_MAGENTA = pygame.image.load(os.path.join('assets','03.png'))
GREAT_LASER_MAGENTA = pygame.image.load(os.path.join('assets','13.png'))
SMALL_LASER_MAGENTA_D = pygame.image.load(os.path.join('assets','03 D.png'))
GREAT_LASER_MAGENTA_D = pygame.image.load(os.path.join('assets','13 D.png'))
##!

##! Verde
SMALL_LASER_GREEN = pygame.image.load(os.path.join('assets','09.png'))
GREAT_LASER_GREEN = pygame.image.load(os.path.join('assets','16.png'))
SMALL_LASER_GREEN_D = pygame.image.load(os.path.join('assets','09 D.png'))
GREAT_LASER_GREEN_D = pygame.image.load(os.path.join('assets','16 D.png'))
##!

##! Demigod Bullet
DEMIGOD_BULLET = pygame.image.load(os.path.join('assets','49.png'))
DEMIGOD_BULLET_D = pygame.image.load(os.path.join('assets','49 D.png'))
##!

##! God Bullet
GOD_BULLET = pygame.image.load(os.path.join('assets','57.png'))
GOD_BULLET_D = pygame.image.load(os.path.join('assets','57 D.png'))
##!
#*}

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets','background.jpg')),(LARGURA,ALTURA))
##!

##?}

#? ANCHOR Classes

class Laser:
    def __init__(self, x, y, img):
        self.x = x-40
        self.y = y-40
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_asset = None
        self.laser_asset = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_asset, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(ALTURA):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_asset)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_asset.get_width()

    def get_height(self):
        return self.ship_asset.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_asset = SPACE_SHIP_PLAYER
        self.laser_asset = SMALL_LASER_PURPLE
        self.mask = pygame.mask.from_surface(self.ship_asset)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(ALTURA):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_asset.get_height() + 10, self.ship_asset.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_asset.get_height() + 10, self.ship_asset.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    CATEGORIES = {'common enemy 1' : (COMMON_ENEMY,SMALL_LASER_BLUE_D,1000), 'common enemy 2' : (COMMON_ENEMY_2,SMALL_LASER_GREEN_D,1300),
                    'cat_6' : (CAT_6_PURPLE_ENEMY,SMALL_LASER_PURPLE_D,2000),'cat_5' : (CAT_5_PURPLE_ENEMY,SMALL_LASER_MAGENTA_D,2300),
                    'cat_4' : (CAT_4_PURPLE_ENEMY,GREAT_LASER_BLUE_D,3000),'cat_3_p' : (CAT_3_PURPLE_ENEMY,GREAT_LASER_PURPLE_D,3300),
                    'cat_3_t' : (CAT_3_TOURM_ENEMY,GREAT_LASER_RED_D,4000), 'cat_2_c' : (CAT_2_CUT_ENEMY,DEMIGOD_BULLET_D,4500),
                    'cat_2_b' : (CAT_2_BOWL_ENEMY,DEMIGOD_BULLET_D,5000), 'demigod' : (CAT_1_DEMIGOD_ENEMY,DEMIGOD_BULLET_D,5500),
                    'god' : (GOD_ENEMY,GOD_BULLET_D,7000)
                }

    def __init__(self, x, y, category,health=1000) -> None:
        super().__init__(x, y, health)
        self.ship_asset,self.laser_asset,self.health = self.CATEGORIES[category]
        self.mask = pygame.mask.from_surface(self.ship_asset)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_asset)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 10
    main_font = pygame.font.Font('ARLRDBD.TTF',20)
    lost_font = pygame.font.Font('ARLRDBD.TTF',50)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 10
    laser_vel = 5

    player = Player(280, 1000)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        TELA.blit(BACKGROUND, (0,0))
        # draw text
        lives_label = main_font.render(f"Vidas: {lives}", 1, (255,0,128))
        level_label = main_font.render(f"Level: {level}", 1, (200,50,0))

        TELA.blit(lives_label, (10, 10))
        TELA.blit(level_label, (LARGURA - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(TELA)

        player.draw(TELA)

        if lost:
            lost_label = lost_font.render("Você perdeu", 1, (255,255,255))
            TELA.blit(lost_label, (LARGURA/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                if level <= 1:
                    enemy = Enemy(random.randrange(70,LARGURA-70),random.randrange(-1500,-100),random.choice(['common enemy 1','common enemy 2']))
                    enemies.append(enemy)
                elif 1 < level <= 5:
                    enemy = Enemy(random.randrange(70,LARGURA-70),random.randrange(-1500,-100),random.choice(['common enemy 1','common enemy 2','cat_6']))
                    enemies.append(enemy)
                elif 5 < level <= 10:
                    enemy = Enemy(random.randrange(70,LARGURA-70),random.randrange(-1500,-100),random.choice(['cat_6','cat_5']))
                    enemies.append(enemy)
                elif 10 < level <= 15:
                    enemy = Enemy(random.randrange(70,LARGURA-70),random.randrange(-1500,-100),random.choice(['cat_4','cat_3_p','cat_3_t']))
                    enemies.append(enemy)
                elif 15 < level <= 20:
                    enemy = Enemy(random.randrange(70,LARGURA-70),random.randrange(-1500,-100),random.choice(['cat_2_c','cat_2_b']))
                    enemies.append(enemy)
                elif 20 < level <= 25:
                    enemy = Enemy(random.randrange(70,LARGURA-70),random.randrange(-1500,-100),random.choice(['demigod','god']))
                    enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and  player.x - player_vel > 0: #* Esquerda
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < LARGURA: #* Direita
            player.x += player_vel
        if keys[pygame.K_w] and  player.y - player_vel > 0: #* Cima
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < ALTURA: #* Baixo
            player.y += player_vel
        if keys[pygame.K_LEFT]  and player.x - player_vel > 0: #* Esquerda SETA
            player.x -= player_vel
        if keys[pygame.K_RIGHT]  and player.x + player_vel + player.get_width() < LARGURA: #* Direita SETA
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: #* Cima SETA
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < ALTURA: #* Baixo SETA
            player.y += player_vel
        
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > ALTURA:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.Font("ARLRDBD.TTF", 70)
    run = True
    while run:
        TELA.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Pressione ENTER", 1, (255,255,255))
        TELA.blit(title_label, (LARGURA/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
    pygame.quit()


main_menu()