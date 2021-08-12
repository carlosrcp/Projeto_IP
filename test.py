#teste de commit
import pygame
from sys import exit

pygame.init()

screen_height = 360
screen_width = 640

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("nome teste")

# loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    pygame.display.update()
gig
    


#fim do teste 2