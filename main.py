#from _typeshed import Self
from math import sin
import pygame
from sys import exit
from math import floor
from pygame import draw
from pygame import key
from pygame import time
from pygame import fastevent
from pygame import sprite
from pygame.constants import ACTIVEEVENT, FULLSCREEN, GL_CONTEXT_RELEASE_BEHAVIOR_FLUSH, KEYDOWN, RESIZABLE
from pygame.display import update
from pygame.math import disable_swizzling

from pygame.mixer import fadeout
import random

from pygame.sprite import Sprite
pygame.init()

# GAME STATES
STATE_MENU = 0
STATE_RUN = 1

last_state = -1
current_state = STATE_MENU

# resolução da tela em pixels
screen_height = 360
screen_width = 640

alien_cooldown = 1000 # recarge do projetil dos aliens em ms
last_enemy_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0

# posicao inicial do primeiro inimigo
x_pos = 250
y_pos = 20

# fonts
standard_font = pygame.font.Font(None, 30)
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)


wave_timer = 0.0

# definindo cores
white = (255, 255, 255)
red = (255, 0, 0)
green = (0,255,0)

# tamanho dos quadrados inimigos (pode ser retirado no momento que forem adicionados as imagens de inimigos)
square_sizes = [11,15,19,20]

# usado para dar spawn de powerups
kill_count = 0

# dificuldade padrao
standard_dificulty = 0

# inimigos mortos/ variavel criada para alterar a dificuldade conforme os inimigos forem mortos
enemies_killed = 0

# contadores
ondas = 0
enemies_killed_total = enemies_killed
current_dificulty = standard_dificulty

# a largura disponível pra a área jogável
playable_width = 202

# variaveis pra ajudar a achar os cantos da area jogavel
playable_area_right = int((screen_width + playable_width)/2)
playable_area_left = int((screen_width - playable_width)/2)
playable_area_center = int(screen_width)/2

# framerate maximo da janela
max_fps = 60

# cria a tela em que o jogo é mostrado, pode variar de  tamanho
screen = pygame.display.set_mode((screen_width,screen_height),pygame.RESIZABLE)
# cria tela em que o jogo é desenhado, sempre tem o mesmo tamanho
game_screen = screen.copy()

# o nome da janela
pygame.display.set_caption("Alien Attack")
icon_game = pygame.image.load("assets/class3.png")
pygame.display.set_icon(icon_game)
# cria o clock que regula o framerate
clock = pygame.time.Clock()

# surface do fundo, tem o tamanho da tela e é toda preta
bg_surface = pygame.Surface((screen_width,screen_height))
bg_surface.fill('black')

# borda da área jogavel
border_group = pygame.sprite.Group()

# definindo uma funcao para desenha texto
def draw_text(text, font, tex_col, x, y):
    img = font.render(text,True, tex_col)
    game_screen.blit(img, (x,y))

def draw_text1(text, font, tex_col, x, y):
    img = font.render(text,True, tex_col)
    game_screen.blit(img, (x,y))

for i in range(1 + int (screen_height / 16)):
    # sprite da borda da direita
    border = Sprite()
    border.image = pygame.image.load('./assets/border.png')
    border.rect = border.image.get_rect()
    border.rect.topleft = (playable_area_right , i * border.rect.height)
    
    # sprite da borda da esquerda
    border_r = Sprite()
    border_r.image = pygame.transform.rotate(pygame.image.load('./assets/border.png'), 180)
    border_r.rect = border.image.get_rect()
    border_r.rect.topright = (playable_area_left , i * border.rect.height)

    border_group.add(border)
    border_group.add(border_r)

# posição inicial
obj_pos = (640 / 2,360 / 2)

bg_group = pygame.sprite.Group()

# fundo principal (estático)
bg_main = Sprite()
bg_main.image = pygame.image.load('./assets/bg.png')
bg_main.rect = bg_main.image.get_rect()
bg_main.rect.topleft = (playable_area_left, 0)

bg_group.add(bg_main)

# paralax vai se mover pra dar ilusão de movimento
paralax_group = pygame.sprite.Group()

for i in range(2):
    parallax_1 = Sprite()
    parallax_1.image = pygame.image.load('./assets/poeira 1.png')
    parallax_1.rect = bg_main.image.get_rect()
    parallax_1.rect.topleft = (playable_area_left, parallax_1.rect.height * i)

    # velocidade em que o vai se mover na tela
    parallax_1.speed = 1

    parallax_2 = Sprite()
    parallax_2.image = pygame.image.load('./assets/poeira 2.png')
    parallax_2.rect = bg_main.image.get_rect()
    parallax_2.rect.topleft = (playable_area_left, parallax_2.rect.height * i)

    parallax_2.speed = 2

    paralax_group.add(parallax_1)
    paralax_group.add(parallax_2)


# função para desenhar o background, coisas a mais como estrelas ao fundo devem ser adicionados aqui
def draw_bg():
    #game_screen.blit(bg_surface, (0,0))

    bg_group.draw(game_screen)

    # movimento do paralax
    for p in paralax_group:
        p.rect.y += p.speed

        if p.rect.y > screen_height/2 + p.rect.height / 2:
            p.rect.y -= p.rect.height * 2

    paralax_group.draw(game_screen)


    #for i in range(screen_height/border.rect.height):
    #    game_screen.blit(border, (0, i * border.rect.height))

# função para desenhar as bordas da tela
def draw_borders():
    game_screen.blit(bg_surface, (playable_area_right,0))
    game_screen.blit(bg_surface, (playable_area_left - screen_width,0))

    border_group.draw(game_screen)



# para ser comparados depois
PICKUP_HP = 0
PICKUP_POWERUP1 = 1
PICKUP_POWERUP2 = 2
PICKUP_POWERUP3 = 3

# Pickups
class Pickup (pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/pickup_hp.png")
        self.rect = self.image.get_rect()
        self.rect.center = [-self.rect.width, -self.rect.height]
        self.active = False
        self.speed = 2
        self.pickup_type = PICKUP_HP
        self.timer = 0


    
    def spawn_rand(self):

        self.active = True
        self.rect.center = [random.randint(playable_area_left, playable_area_right - self.rect.width) , 0]
        self.timer = 0

    def spawn(self, x, y):
        self.active = True
        self.rect.center = [x,y]
        self.timer = 0
    
    def update(self):
        if not(self.active):
            return

        #dt = clock.tick(max_fps)
    
        self.timer += 1.0 / max_fps

        self.rect.y += self.speed

        if self.rect.y > screen_height + 16:
            self.active = False
        
        #update mask
        self.mask = pygame.mask.from_surface(self.image)
    
    # quando o personagem pegar o power up
    def pick(self):
        self.disable()

    # pick sai da tela e fica inativa, pode ser usado pra quando você pega e ela sai da tela
    def disable(self):
        self.rect.center = [-self.rect.width, -self.rect.height]
        self.active = False


class Pickup_HP (Pickup):
    def __init__(self) -> None:
        Pickup.__init__(self)
        
        #pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./assets/pickup_hp.png")
        self.pickup_type = PICKUP_HP
    
    
    def pick(self):
        Pickup.pick(self)

        player.health_remaining = min(100, player.health_remaining + 30)

class Pickup_PowerUp1 (Pickup):
    def __init__(self) -> None:
        Pickup.__init__(self)
        
        #pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./assets/pickup_1.png")
        self.pickup_type = PICKUP_POWERUP1
    
    
    def update(self):
        Pickup.update(self)
        
        # zig zag
        if self.active:
            speed_x = int (sin(self.timer * 6) * 3)
            self.rect.x += speed_x
    
    def pick(self):
        Pickup.pick(self)

        player.machinegun_up()

class Pickup_PowerUp2 (Pickup):
    def __init__(self) -> None:
        Pickup.__init__(self)
        
        #pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./assets/pickup_3.png")
        self.pickup_type = PICKUP_POWERUP2
    
    
    def update(self):
        Pickup.update(self)
        
        # zig zag
        if self.active:
            speed_x = int (sin(self.timer * 6) * 3)
            self.rect.x += speed_x
    
    def pick(self):
        Pickup.pick(self)

        player.shotgun_up()

class Pickup_PowerUp3 (Pickup):
    def __init__(self) -> None:
        Pickup.__init__(self)
        
        #pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./assets/pickup_2.png")
        self.pickup_type = PICKUP_POWERUP3
    
    
    def update(self):
        Pickup.update(self)
        
        # zig zag
        if self.active:
            speed_x = int (sin(self.timer * 6) * 3)
            self.rect.x += speed_x

pickups_group = pygame.sprite.Group()

for i in range(3):
    new_pu = Pickup_HP()
    pickups_group.add(new_pu)

for i in range(3):
    new_pu = Pickup_PowerUp1()
    pickups_group.add(new_pu)

for i in range(3):
    new_pu = Pickup_PowerUp2()
    pickups_group.add(new_pu)

for i in range(3):
    new_pu = Pickup_PowerUp3()
    pickups_group.add(new_pu)



# classe do projetil
class Projectile (pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/projectilec2.png")
        self.rect = self.image.get_rect()
        self.rect.center = [-self.rect.width, -self.rect.height]

        # se shot for falso, significa que o projetil está inativo e pode ser disparado
        self.shot = False
        self.speed_x = 0
    
    def update(self):
        
        # se o projetil tiver sido disparado
        if self.shot:
            speed = 5
            self.rect.y -= speed
            self.rect.x += self.speed_x
        
        # se o projetil sair da tela, ficar inativo
        if self.shot and self.rect.y < - 16:
            self.disable()
            #self.shot = False
        
        hits = pygame.sprite.spritecollide(self,enemies_group, False)
        #if pygame.sprite.spritecollide(self,enemies_group,True):
        for hit in hits:
            if self.shot:
                self.disable()
                
                pygame.mixer.Sound('./assets/Explosion.wav').play()
                hit.die()
                #break
    
    def disable(self):
        self.rect.center = [-self.rect.width, -self.rect.height]
        self.shot = False



# grupo que guarda os projeteis a ser disparados
projectile_group = pygame.sprite.Group()

def create_projectiles(value: int):
    for i in range(value): # em range(X), x é o número de projeteis
    # projetil é criado fora da tela e adicionado ao grupo
        new_projectile = Projectile()

        projectile_group.add(new_projectile)

create_projectiles(60)

class Alien_Projectile (pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/projectiled.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        
        if pygame.sprite.spritecollide(self,player_group,False):
            self.kill()
            player.health_remaining -= 50
            pygame.mixer.Sound('assets/Explosion_1.wav').play()

enemies_projectile_group = pygame.sprite.Group()

health_font = pygame.font.SysFont('comicsans', 30)

#função que contem os textos com os atributos atuais
def text(health):
    #textos a esquerda
    health_text = health_font.render("Health: " + str(health), True, white)

    #textos a direita
    #direita_text = health_font.render("Texto a direita: " + str(health), 1, white)
    #bg_surface.blit(direita_text, (screen_width - direita_text.get_width() - 10, 10))

    return health_text

# classe da nave do jogador 
class Player (pygame.sprite.Sprite):
    
    def __init__(self, x, y,health) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/nave.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.health_remaining = health
        self.trigger = False

        
        self.machinegun_list = [40,32,26,20,16,12,10]
        self.machinegun_level = 0
        self.reload_rate = self.machinegun_list[0]
        self.reload_count = self.reload_rate

        self.shotgun_list = [14,12,10,8,6,4,2]
        self.shotgun_level = 0
        self.shotgun_rate = self.shotgun_list[0]
        self.shotgun_count = self.shotgun_rate

        self.active = True

    def reset(self):
        self.rect.x = playable_area_center
        self.health_remaining = 100
        self.trigger = False
        self.active = True

        self.machinegun_level = 0
        self.reload_rate = self.machinegun_list[0]
        self.reload_count = self.reload_rate

        self.shotgun_level = 0
        self.shotgun_rate = self.shotgun_list[0]
        self.shotgun_count = self.shotgun_rate


    # atirar se houve projetile disponivel
    def shoot(self, speed_x):
        for i in projectile_group:
            if i.shot == False:
                # tiro foi disparado
                i.rect.x = self.rect.x
                i.rect.y = self.rect.y
                i.shot = True
                i.speed_x = speed_x

                self.reload_count = self.reload_rate                    
                
                pygame.mixer.Sound('./assets/Laser_shoot.wav').play()  # adiciona pew pew pew
                return
    
    def shoot_shotgun(self):
        self.shotgun_count = self.shotgun_rate
        self.shoot(0)
        self.shoot(1)
        self.shoot(-1)

    def machinegun_up(self):
        #self.machinegun_level += 1
        self.machinegun_level = min(self.machinegun_level + 1, len(self.machinegun_list) - 1)

        self.reload_rate = self.machinegun_list[self.machinegun_level]

        #if self.machinegun_level == 1:
        #    self.reload_rate = 16
        #elif self.machinegun_level == 2:
        #    self.reload_rate = 12
        #elif self.machinegun_level == 3:
        #    self.reload_rate = 8
        #elif self.machinegun_level == 4:
        #    self.reload_rate = 6
    
    
    def shotgun_up(self):
        self.shotgun_level = min(self.shotgun_level + 1, len(self.shotgun_list) - 1)

        self.shotgun_rate = self.shotgun_list[self.shotgun_level]
        

        #if self.shotgun_level == 1:
        #    self.shotgun_rate = 5
        #elif self.shotgun_level == 2:
        #    self.shotgun_rate = 4
        #elif self.shotgun_level == 3:
        #    self.shotgun_rate = 3
        #elif self.shotgun_level == 4:
        #    self.shotgun_rate = 2
    
    # update que é chamado a cada frame
    def update(self):
        
        self.reload_count = max(0, self.reload_count - 1)

        # velocidade da nave, precisa ser ajustada em diagonais        
        speed = 4

        # checa e inputs e faz o movimento
        key_pressed = pygame.key.get_pressed()
        

        # movimento horizontal
        if key_pressed[pygame.K_LEFT]:
            self.rect.x = max(self.rect.x - speed, playable_area_left)  #self.rect.x -= speed 

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x = min(self.rect.x + speed, playable_area_right - self.rect.width)
        
        # Movimento vertical 
        #if key_pressed[pygame.K_UP]:
        #    self.rect.y = max(self.rect.y - speed, 0)#
        #if key_pressed[pygame.K_DOWN]:
        #    self.rect.y = min(self.rect.y + speed, screen_height - 16) 
        
        # checa e dispara os projeteis
        if key_pressed[pygame.K_SPACE] and self.active:
            
            if (not(self.trigger) and self.reload_count < 10) or self.reload_count == 0:
                if self.shotgun_count == 0 and self.shotgun_level > 0:
                    self.shoot_shotgun()
                else:
                    self.shoot(0)
                    self.shotgun_count = max(0, self.shotgun_count - 1)

            self.trigger = True
        else:
            self.trigger = False


# cria um drop na posicao x, y
def spawn_drop(x, y):
    
    drop_type = PICKUP_HP
    
    # se tiver com a vida cheia dropar power up, se não dropar vida
    if player.health_remaining == 100:
        rand = random.randint(0,1)

        if rand == 0:
            drop_type = PICKUP_POWERUP1
        elif rand == 1:
            drop_type = PICKUP_POWERUP2
        else:
            drop_type = PICKUP_POWERUP3

    for p in pickups_group:
        if p.pickup_type == drop_type and not(p.active):
            p.spawn(x,y)
            
            break



class EnemySquare(pygame.sprite.Sprite):
    def __init__(self,type,x_adjust,y_adjust):
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.moving_counter = 0
        self.enemy_speed = 1
        index_class = 0

        self.offset = screen_height

        classes = ['assets/class1.png','assets/class2.png','assets/class3.png']
        
        if y_adjust == 0 or y_adjust == 1:
            index_class = 0
        elif y_adjust == 2 or y_adjust == 3:
            index_class = 1
        elif y_adjust == 4 or y_adjust == 5:
            index_class = 2

        self.image = pygame.image.load(classes[index_class])
        # self.image = pygame.image.load((square_sizes[type],square_sizes[type]))
        # self.image.fill((150,64,64))
        self.rect = self.image.get_rect(center = (self.x + (x_adjust*(square_sizes[2] + 9)),self.y + (y_adjust*(square_sizes[2] + 9))))
        self.rect.y -= self.offset
    
    def update(self,ind: int):
        self.dificulties = [1,2,4,8,16,32,64,128]
        self.time = 2 + floor(pygame.time.get_ticks()/100)
        
        if self.offset > 0:
            delta = min(self.offset, 10)
            self.offset -= delta
            self.rect.y += delta

        # ####### timer criado com proposito de teste #########
        # self.time_display = standard_font.render(f'timer: {self.time}',False,'White')
        # screen.blit(self.time_display,(10,100))

        if self.time == int(self.time) and self.time % (16/self.dificulties[ind]) == 0:
            self.rect.x += self.enemy_speed
            self.moving_counter += 1
            if abs(self.moving_counter) >= 22:
                self.rect.y += 4
                self.enemy_speed *= -1
                self.moving_counter *= self.enemy_speed
    
    # chamada quando o inimigo for atingido e morrer
    def die(self):
        global enemies_killed
        enemies_killed += 1
        global enemies_killed_total
        enemies_killed_total += 1
        global kill_count
        kill_count += 1

        if kill_count > 5:
            kill_count = 0
            spawn_drop(self.rect.x, self.rect.y)
        
        self.kill()

enemies_group = pygame.sprite.Group()

def create_enemies(waves: int):
    if waves > 4:
        waves = 4
    for j in range(6):
        for i in range(6):
            enemies_group.add(EnemySquare(floor(j/2),i,j + waves))

create_enemies(0)

# grupo dos jogadores, só tem 1
player_group = pygame.sprite.Group()

# cria o jogador na posição inicial
player = Player(int(screen_width/2), 9 * int(screen_height/10), 100)
player_group.add(player)


# timer para dropar os pickups, apenas para fins de testes
timer = 0.0

# temporario so pra testar os pickups caindo
#comp_test = 0


def reset():
    for i in enemies_group:
        i.kill()
    for i in enemies_projectile_group:
        i.kill()
    
    for i in pickups_group:
        i.disable()
    for i in projectile_group:
        i.disable()
    
    
    player.reset()



# def game_over():

# apenas desenha um menu com 2 opcoes
def main_menu():
    
    global timer
    ## carrega e toca a música
    ## # sujeito a mudnça caso menu seja implementado
    #pygame.mixer.music.load("assets/menu_0.wav")
    #pygame.mixer.music.play(-1)
    #pygame.mixer.music.set_volume(1.0)

    run = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    game_screen.blit(bg_surface,(0,0))
    
    bg_group.draw(game_screen)
    # movimento do paralax
    for p in paralax_group:
        p.rect.y += p.speed
        if p.rect.y > screen_height/2 + p.rect.height / 2:
            p.rect.y -= p.rect.height * 2
    paralax_group.draw(game_screen)
    border_group.draw(game_screen)
    
    pickups_group.draw(game_screen)
    projectile_group.draw(game_screen)    
    player_group.draw(game_screen)
    enemies_group.draw(game_screen)
    
    #pickups_group.update()
    #player_group.update()
    #projectile_group.update()
    # enemies_group.update(current_dificulty)
    
    draw_text('1 - Start',font40, white,50,200)
    draw_text('2 - Exit',font40, white,50,250)
    
    menu_key = pygame.key.get_pressed()
    
    if menu_key[pygame.K_1]:        
        global current_state
        current_state = STATE_RUN
        #pygame.mixer.music.unload()
        #run = game()
        
    if menu_key[pygame.K_2]:
        #run = False
        quit()
    
    # aumenta o tamanho da game_screen e desenha ela na screen
    screenshot = pygame.transform.scale(game_screen, screen.get_rect().size)
    screen.blit(screenshot, (0,0))
    
    pygame.display.update()


current_dificulty = 0

def game():
    global ondas
    #ondas = 0
    global countdown
    #countdown = 3
    global timer
    #timer = 0.0
    global enemies_killed
    #enemies_killed = 0
    global last_count
    global comp_test
    #comp_test = 0
    global last_enemy_shot
    global game_over
    #game_over = 0

    global wave_timer
    global current_dificulty
    
    #pygame.mixer.music.load("assets/Space_0.wav")
    #pygame.mixer.music.play(-1)
    #pygame.mixer.music.set_volume(1.0)
    
    running = True
# loop principal
    #while running:
        
    # fecha a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            return False
    
    enemy_list = enemies_group.sprites()
    if enemy_list == []:
        enemy_list = False
    # checa de o jogador ainda esta vivo
    if enemy_list:
        global current_state
        global STATE_MENU
        if player.health_remaining <= 0 or enemy_list[len(enemy_list)-1].rect.centery >=  9 * int(screen_height/10):
            player.health_remaining = 0
            # global current_state
            # global STATE_MENU
            current_state =  STATE_MENU
            reset()
            return
            game_over = -1
    else:
        if player.health_remaining <= 0:
            player.health_remaining = 0
            # global current_state
            # global STATE_MENU
            current_state =  STATE_MENU
            reset()
            return
            game_over = -1

    # dt é o delta time, o tempo de um frame para o outro
    dt = clock.tick(max_fps)

    timer += dt / 1000.0
    
    # altera a dificuldade
    if enemies_killed == 0:
        current_dificulty = 0 + ondas
    elif enemies_killed < 32:
        current_dificulty = floor(enemies_killed/8) + ondas
        if current_dificulty > 7:
            current_dificulty = 7
    
    # checa se existe grupo de inimigos
    if not enemies_group:
        player.active = False
        wave_timer += 1.0/60
        
        
        if wave_timer > 4:
            if ondas < 6:
                ondas += 1
            current_dificulty -= 2
            enemies_killed = 0
            wave_timer = 0.0
            player.active = True
            #pygame.time.delay(500)
            create_enemies(ondas)
    if countdown == 0:
        time_now = pygame.time.get_ticks()
        if time_now - last_enemy_shot > alien_cooldown and len(enemies_group) > 0:
            attacking_enemy = random.choice(enemies_group.sprites())
            enemy_projectile = Alien_Projectile(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom)
            enemies_projectile_group.add(enemy_projectile)
            last_enemy_shot = time_now    
        if game_over == 0:
            # update nos projeteis,jogador e inimigos
            pickups_group.update()
            player_group.update()
            projectile_group.update()
            enemies_group.update(current_dificulty)
            enemies_projectile_group.update()
        else:
            draw_text1('GAME OVER',font40, white, playable_area_center-110, 200 )
            
            running = False
            return False
            # pygame.mixer.music.unload()
            #  running = False
            
            #  enemies_group.empty()
            #  create_enemies(0)
            
            # projectile_group.empty()
            #  create_projectiles(3)
            
            # pickups_group.empty()
            # for i in range(3):
            #     new_pu = Pickup_HP()
            #      pickups_group.add(new_pu)
            # for i in range(3):
            #     new_pu = Pickup_PowerUp1()
            #     pickups_group.add(new_pu)
            # for i in range(3):
            #  #     pickups_group.add(new_pu)
            # for i in range(3):
            #     new_pu = Pickup_PowerUp3()
            #     pickups_group.add(new_pu)
            
            # player_group.empty()
            # player = Player(int(screen_width/2), 9 * int(screen_height/10), 100)
            #  player_group.add(player)
            
            # main_menu(False)
    
    # REMOVER
    # criacao dos pickups, coloquei essa comp_test pra testar todos os tipos
    #if timer > 3:
    #    timer = 0
    #
    #    for pu in pickups_group:
    #        if pu.active == False and pu.pickup_type == comp_test:
    #            pu.spawn_rand()
    #
    #            break
    #
    #    comp_test +=1
    #
    #    if comp_test > 3:
    #        comp_test = 0

    # as chamadas de draw devem ser feitas de trás pra frente
    # começando pelo fundo e terminando pelo jogador
    # desenha o fundo (tela preta)
    draw_bg()

    # desenha os projeteis, inimigos e o jogador
    pickups_group.draw(game_screen)
    projectile_group.draw(game_screen)    
    player_group.draw(game_screen)
    enemies_group.draw(game_screen)
    enemies_projectile_group.draw(game_screen)
    
    # draw top
    draw_borders()
    
    # aviso de próxima wave
    if wave_timer % 0.4 > 0.2:
        draw_text(f'wave {ondas+2} !',font40, white, playable_area_center-55, 100 )
    if countdown > 0:
        draw_text1('GET READY!', font40, white, playable_area_center-110, 200)
        draw_text1(str(countdown), font40, white, playable_area_center-10, 250)
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
    
    
    #checar se pegou pickup
    # alterei aqui para ao inves de remover o sprite ele chamar o metodo disable
    # assim ele não é removido, e sim desabilitado e fica pronto par ser usado de novo
    pu_collisions = pygame.sprite.spritecollide(player, pickups_group, False)
    for col in pu_collisions:
        if col.active:
            col.pick()           
    
    # hp_sfx = pygame.mixer.Sound("assets/HP.wav")
    # pygame.mixer.Sound.play(hp_sfx)
    # função com os textos
    txt_health = text(player.health_remaining)
    game_screen.blit(txt_health, (10,10))
    dificulty_display = standard_font.render(f'Level: {current_dificulty}',False,'White')
    game_screen.blit(dificulty_display, (10,50))
    enemies_display = standard_font.render(f'Kills: {enemies_killed_total}',False,'White')
    game_screen.blit(enemies_display, (10,90))
    waves_display = standard_font.render(f'Wave: {ondas+1}',False,'White')
    game_screen.blit(waves_display, (10,130))
    lvl1 = player.machinegun_level if player.machinegun_level < len(player.machinegun_list) - 1 else 'max'
    powerup1_display = standard_font.render(f'Speed lvl: {lvl1}',False,'White')
    game_screen.blit(powerup1_display, (playable_area_right + 20, screen_height - 70))
    
    lvl2 = player.shotgun_level if player.shotgun_level < len(player.shotgun_list) - 1 else 'max'
    powerup2_display = standard_font.render(f'Shotgun lvl: {lvl2}',False,'White')
    game_screen.blit(powerup2_display, (playable_area_right + 20, screen_height - 40))
    # aumenta o tamanho da game_screen e desenha ela na screen
    screenshot = pygame.transform.scale(game_screen, screen.get_rect().size)
    screen.blit(screenshot, (0,0))
    
    pygame.display.update()

#main_menu()



def start_menu():
    # carrega e toca a música
    # # sujeito a mudnça caso menu seja implementado
    pygame.mixer.music.load("assets/menu_0.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)

def start_game():
    global ondas
    ondas = 0
    global countdown
    countdown = 3
    global timer
    timer = 0.0
    global enemies_killed
    enemies_killed = 0
    global last_count
    global comp_test
    comp_test = 0
    global last_enemy_shot
    global game_over
    game_over = 0

    global wave_timer
    
    print('game start')
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/Space_0.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

            #running = False
            #return False

    if current_state == STATE_MENU:
        if last_state != current_state:
            start_menu()
            
        last_state = current_state

        main_menu()
    elif current_state == STATE_RUN:        
        if last_state != current_state:
            start_game()
        
        last_state = current_state
        
        game()
    


def quit():
    pygame.quit()
    exit()




pygame.quit()
exit()
# gig