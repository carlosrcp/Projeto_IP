#from _typeshed import Self
import pygame
from sys import exit
from pygame import draw
from pygame import key
from pygame import time
from pygame import fastevent
from pygame import sprite
from pygame.constants import FULLSCREEN, KEYDOWN, RESIZABLE
from pygame.display import update

from pygame.mixer import fadeout
import random

from pygame.sprite import Sprite
pygame.init()

# resolução da tela em pixels
screen_height = 360
screen_width = 640

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
pygame.display.set_caption("nome teste")
# cria o clock que regula o framerate
clock = pygame.time.Clock()

# surface do fundo, tem o tamanho da tela e é toda preta
bg_surface = pygame.Surface((screen_width,screen_height))
bg_surface.fill('black')




# borda da área jogavel
border_group = pygame.sprite.Group()

for i in range(1 + int (screen_height / 16)):
    # sprite da borda da direita
    border = Sprite()
    border.image = pygame.image.load('assets/border.png')
    border.rect = border.image.get_rect()
    border.rect.topleft = (playable_area_right , i * border.rect.height)    
    
    # sprite da borda da esquerda
    border_r = Sprite()
    border_r.image = pygame.transform.rotate(pygame.image.load('assets/border.png'), 180)
    border_r.rect = border.image.get_rect()
    border_r.rect.topright = (playable_area_left , i * border.rect.height) 

    border_group.add(border)
    border_group.add(border_r)

# posição inicial
obj_pos = (640 / 2,360 / 2)


bg_group = pygame.sprite.Group()

# fundo principal (estático)
bg_main = Sprite()
bg_main.image = pygame.image.load('assets/bg.png')
bg_main.rect = bg_main.image.get_rect()
bg_main.rect.topleft = (playable_area_left, 0)

bg_group.add(bg_main)

# paralax vai se mover pra dar ilusão de movimento
paralax_group = pygame.sprite.Group()

for i in range(2):
    parallax_1 = Sprite()
    parallax_1.image = pygame.image.load('assets/poeira 1.png')
    parallax_1.rect = bg_main.image.get_rect()
    parallax_1.rect.topleft = (playable_area_left, parallax_1.rect.height * i)

    # velocidade em que o vai se mover na tela
    parallax_1.speed = 1

    parallax_2 = Sprite()
    parallax_2.image = pygame.image.load('assets/poeira 2.png')
    parallax_2.rect = bg_main.image.get_rect()
    parallax_2.rect.topleft = (playable_area_left, parallax_2.rect.height * i)

    parallax_2.speed = 2

    paralax_group.add(parallax_1)
    paralax_group.add(parallax_2)





# função para desenhar o background, coisas a mais como estrelas ao fundo devem ser adicionados aqui
def draw_bg():
    game_screen.blit(bg_surface, (0,0))

    bg_group.draw(game_screen)

    # movimento do paralax
    for p in paralax_group:
        p.rect.y += p.speed

        if p.rect.y > screen_height/2 + p.rect.height / 2:
            p.rect.y -= p.rect.height * 2

    paralax_group.draw(game_screen)

    border_group.draw(game_screen)

    #for i in range(screen_height/border.rect.height):
    #    game_screen.blit(border, (0, i * border.rect.height))


# Pickups
class Pickup (pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/pickup_hp.png")
        self.rect = self.image.get_rect()
        self.rect.center = [-self.rect.width, -self.rect.height]
        self.active = False
        self.speed = 3
    
    def spawn_rand(self):

        self.active = True
        self.rect.center = [random.randint(playable_area_left, playable_area_right - self.rect.width) , 0]

    def spawn(self, x, y):
        self.active = True
        self.rect.center = [x,y]
    
    def update(self):
        if not(self.active):
            return

        self.rect.y +=self.speed

        if self.rect.y > screen_height + 16:
            self.active = False

        

pickups_group = pygame.sprite.Group()

for i in range(3):
    new_pu = Pickup()
    pickups_group.add(new_pu)


# classe do projetil
class Projectile (pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("projectile.png")
        self.rect = self.image.get_rect()
        self.rect.center = [-self.rect.width, -self.rect.height]

        # se shot for falso, significa que o projetil está inativo e pode ser disparado
        self.shot = False
    
    def update(self):
        
        # se o projetil tiver sido disparado
        if self.shot:
            speed = 8
            self.rect.y -= speed
        
        # se o projetil sair da tela, ficar inativo
        if self.rect.y < - 16:
            self.shot = False
        

# grupo que guarda os projeteis a ser disparados
projectile_group = pygame.sprite.Group()
for i in range(3): # em range(X), x é o número de projeteis
    # projetil é criado fora da tela e adicionado ao grupo
    new_projectile = Projectile()

    projectile_group.add(new_projectile)


# classe da nave do jogador 
class Player (pygame.sprite.Sprite):
    
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("nave.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.trigger = False
    

    # atirar se houve projetile disponivel
    def shoot(self):
        for i in projectile_group:
            if i.shot == False:
                # tiro foi disparado
                i.rect.x = self.rect.x
                i.rect.y = self.rect.y
                i.shot = True
                
                pygame.mixer.Sound('assets/Laser_shoot.wav').play()  # adiciona pew pew pew
                return

    # update que é chamado a cada frame
    def update(self):

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
        if key_pressed[pygame.K_SPACE]:
            
            if not(self.trigger):
                self.shoot()

            self.trigger = True
        else:
            self.trigger = False


# grupo dos jogadores, só tem 1
player_group = pygame.sprite.Group()

# cria o jogador na posição inicial
player = Player(int(screen_width/2), 9 * int(screen_height/10))
player_group.add(player)

# timer para dropar os pickups, apenas para fins de testes
timer = 0.0

# loop principal
while True:

    # fecha a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # dt é o delta time, o tempo de um frame para o outro
    dt = clock.tick(max_fps)
    
    timer += dt / 1000.0

    # update nos projeteis e jogador
    pickups_group.update()
    player_group.update()
    projectile_group.update()
    

    # criacao dos pickups
    if timer > 4:
        timer = 0

        for pu in pickups_group:
            if pu.active == False:
                pu.spawn_rand()

                break


    # as chamadas de draw devem ser feitas de trás pra frente
    # começando pelo fundo e terminando pelo jogador

    # desenha o fundo (tela preta)
    draw_bg()

    # desenha os projeteis e o jogador
    pickups_group.draw(game_screen)
    projectile_group.draw(game_screen)    
    player_group.draw(game_screen)


    # aumenta o tamanho da game_screen e desenha ela na screen
    screenshot = pygame.transform.scale(game_screen, screen.get_rect().size)

    screen.blit(screenshot, (0,0))
    
    pygame.display.update()


gig