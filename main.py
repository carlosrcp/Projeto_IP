import pygame
from sys import exit

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
bg_surface = pygame.Surface((1,1))
bg_surface.fill('black')

# posição inicial
obj_pos = (640 / 2,360 / 2)

# guardar se o botao está sendo segurado
move_up = False
move_down = False
move_left = False
move_right = False


# loop principal
while True:
    # fecha a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_LEFT:
                move_left = True
            elif event.key== pygame.K_RIGHT:
                move_right = True
            elif event.key== pygame.K_UP:
                move_up = True
            elif event.key== pygame.K_DOWN:
                move_down = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
    
    
    dt = clock.tick(max_fps)
    
    velocidade = 6
    
    if move_down:
        obj_pos = (obj_pos[0], obj_pos[1] + velocidade)
    if move_up:
        obj_pos = (obj_pos[0], obj_pos[1] - velocidade)
    if move_right:
        obj_pos = (obj_pos[0] + velocidade, obj_pos[1])
    if move_left:
        obj_pos = (obj_pos[0] - velocidade, obj_pos[1])

    for x in range(screen_width):
        for y in range(screen_height):
            screen.blit(bg_surface, (x,y))

    screen.blit(test_surface, obj_pos)

    pygame.display.update()
gig
    


#fim do teste 2