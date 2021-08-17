#from _typeshed import Self
import pygame
from sys import exit
from pygame import draw
from pygame import key
from pygame.constants import KEYDOWN
from pygame.display import update

from pygame.mixer import fadeout

pygame.init()

# resolução da tela em pixels
screen_height = 360
screen_width = 640

# framerate maximo da janela
max_fps = 60

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("nome teste")
clock = pygame.time.Clock()

# surface do objeto que se move
test_surface = pygame.Surface((16,16))
test_surface.fill('red')

# surface do fundo
bg_surface = pygame.Surface((screen_width,screen_height))
bg_surface.fill('black')

#img_nave = pygame.image.load("nave.png")

# posição inicial
obj_pos = (640 / 2,360 / 2)

# guardar se o botao está sendo segurado
move_up = False
move_down = False
move_left = False
move_right = False

def draw_bg():
    screen.blit(bg_surface, (0,0))

class Projectile (pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("projectile.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.shot = False
    
    #ready = False
    def update(self):
        
        # se o projetil tiver sido disparado
        if self.shot:
            speed = 8
            self.rect.y -= speed
        
        if self.rect.y < - 16:
            self.shot = False
        

projectile_group = pygame.sprite.Group()
for i in range(3):
    new_projectile = Projectile(0,0)

    projectile_group.add(new_projectile)

class Player (pygame.sprite.Sprite):
        
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("nave.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.trigger = False
    
    def shoot(self):
        for i in projectile_group:
            if i.shot == False:
                i.rect.x = self.rect.x
                i.rect.y = self.rect.y
                i.shot = True
                return

    def update(self):
        
        speed = 6

        key_pressed = pygame.key.get_pressed()
        
        
        #key_down = pygame.KEYDOWN()

        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= speed 

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += speed 
        
        if key_pressed[pygame.K_UP]:
            self.rect.y -= speed 

        if key_pressed[pygame.K_DOWN]:
            self.rect.y += speed 
        
        if key_pressed[pygame.K_SPACE]:
            if not(self.trigger):
                self.shoot()
            
            self.trigger = True
        else:
            self.trigger = False

player_group = pygame.sprite.Group()


player = Player(int(screen_width/2), int(screen_height/2))
player_group.add(player)

# loop principal
while True:
    # fecha a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    
    dt = clock.tick(max_fps)
    
    draw_bg()

    # desenhar os sprites
    player_group.update()
    player_group.draw(screen)

    projectile_group.update()
    projectile_group.draw(screen)


    pygame.display.update()
gig
    


#fim do teste 2