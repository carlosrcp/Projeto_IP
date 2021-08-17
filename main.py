#from _typeshed import Self
import pygame
from sys import exit
from pygame import draw
from pygame import key
from pygame.constants import FULLSCREEN, KEYDOWN, RESIZABLE
from pygame.display import update

from pygame.mixer import fadeout

pygame.init()

# resolução da tela em pixels
screen_height = 360
screen_width = 640

# framerate maximo da janela
max_fps = 60

# cria a tela
screen = pygame.display.set_mode((screen_width,screen_height))
# o nome da janela
pygame.display.set_caption("nome teste")
# cria o clock que regula o framerate
clock = pygame.time.Clock()

# surface do objeto que se move
test_surface = pygame.Surface((16,16))
test_surface.fill('red')

# surface do fundo, tem o tamanho da tela e é toda preta
bg_surface = pygame.Surface((screen_width,screen_height))
bg_surface.fill('black')

# posição inicial
obj_pos = (640 / 2,360 / 2)

# função para desenhar o background, coisas a mais como estrelas ao fundo devem ser adicionados aqui
def draw_bg():
    screen.blit(bg_surface, (0,0))


# classe do projetil
class Projectile (pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("projectile.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

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
    new_projectile = Projectile(0,-10)

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
                i.rect.x = self.rect.x
                i.rect.y = self.rect.y
                i.shot = True
                return

    # update que é chamado a cada frame
    def update(self):

        # velocidade da nave, precisa ser ajustada em diagonais        
        speed = 4

        # checa e inputs e faz o movimento
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_LEFT]:
            self.rect.x = max(self.rect.x - speed, 0)  #self.rect.x -= speed 

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x = min(self.rect.x + speed, screen_width - 16)
        
        if key_pressed[pygame.K_UP]:
            self.rect.y = max(self.rect.y - speed, 0)

        if key_pressed[pygame.K_DOWN]:
            self.rect.y = min(self.rect.y + speed, screen_height - 16) 
        

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
player = Player(int(screen_width/2), int(screen_height/2))
player_group.add(player)

# loop principal
while True:
    # fecha a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # dt é o delta time, o tempo de um tick para o outro
    dt = clock.tick(max_fps)
    
    # update nos projeteis e jogador
    player_group.update()
    projectile_group.update()
    

    # as chamadas de draw devem ser feitas de trás pra frente
    # começando pelo fundo e terminando pelo jogador

    # desenha o fundo (tela preta)
    draw_bg()

    # desenha os projeteis e o jogador
    projectile_group.draw(screen)    
    player_group.draw(screen)

    pygame.display.update()
gig