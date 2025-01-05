# IEE2613 Cañon.
#
# Carlos Stappung 


#################################  IMPORTAMOS LIBRERIAS  #################################
import os
import pygame
from pygame.locals import *
import numpy as np
###########################################################################################
#CLASE PARA CREAR CONTROLADOR PID, PARA MÁS COMODIDAD CON EL GUARDADO DE DATOS

## Función encargada de recibir los comandos ejecutados por la persona (teclado, raton)
def key_press():
    ## Leemos los eventos ejecutados con la funcion event.get() de Pygame
    click = False
    for event in pygame.event.get():
            ## Caso se cierra el programa
            if event.type == pygame.QUIT:
                exit()

            ## Caso de apretar una tecla
            if event.type == pygame.KEYDOWN:
                
                ## Escape para cerrar
                if event.key == pygame.K_ESCAPE:
                    exit()

            ## Leemos el mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                ## Si click izquierdo click true, lo que hace tomar la poscion dentro del codigo
                if event.button == 1:
                    click = True
            
    ## Retornamos todas las variables        
    return click


def update_screen(screen, circles, jugador ,SIZE_CELL, NUM_X_CELL, NUM_Y_CELL, X_MAX, Y_MAX, counter_animate, list_reaction):

    ## ALGUNOS COLORES
    GREEN = (0, 220, 0)
    LIGHT_GREEN = (0, 255, 0)
    BLACK = (0,0,0)
    RED = (220, 0, 0)
    LIGHT_RED = (255, 0, 0)
    blue = (0, 0, 128)  

    ## FONT PARA LOS TEXTOS
    font = pygame.font.Font('freesansbold.ttf', SIZE_CELL//2)

    ## COLOR DEL FONDO
    screen.fill(BLACK)
    ## PASTO
    #pygame.draw.rect(screen,(50,205,50), ( 0 , Y_MAX/2 , X_MAX, Y_MAX/2) )
    #DIBUJAMOS CUADRICULA
    for CORD_X in range(NUM_X_CELL+1):
        for CORD_Y in range(NUM_Y_CELL+1):
            WITHD_LINE = 3
            # Líneas Horizontales
            pygame.draw.line(screen, jugador.color , (SIZE_CELL*(CORD_X+1), SIZE_CELL), (SIZE_CELL*(CORD_X+1), Y_MAX - SIZE_CELL), WITHD_LINE)
            # Líneas Verticales
            pygame.draw.line(screen, jugador.color , (SIZE_CELL, SIZE_CELL*(CORD_Y+1)), (X_MAX - SIZE_CELL, SIZE_CELL*(CORD_Y+1)), WITHD_LINE)
    for circle_list in circles:
        for circle in circle_list:
            if circle.number != 0:
                pygame.draw.circle(screen,  circle.second_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1), SIZE_CELL//2 + SIZE_CELL*(circle.y+1)), (SIZE_CELL*0.7)//2)
                pygame.draw.circle(screen,  circle.main_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1), SIZE_CELL//2 + SIZE_CELL*(circle.y+1)), (SIZE_CELL*0.55)//2)
                ## DISPLAY TEXTO FX
                text_temp= font.render(f'{round(circle.number)}', True, (255,255,255))
                text_temp_Rect = text_temp.get_rect()
                text_temp_Rect.center = (SIZE_CELL//2 + SIZE_CELL*(circle.x+1), SIZE_CELL//2 +  SIZE_CELL*(circle.y+1))
                screen.blit(text_temp, text_temp_Rect)
    
    for circle in list_reaction:
        if circle.x + 1 < NUM_X_CELL:
            pygame.draw.circle(screen,  circle.second_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1) + counter_animate, SIZE_CELL//2 + SIZE_CELL*(circle.y+1)), (SIZE_CELL*0.7)//2)
            pygame.draw.circle(screen,  circle.main_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1) + counter_animate, SIZE_CELL//2 + SIZE_CELL*(circle.y+1)), (SIZE_CELL*0.6)//2)
        
        if circle.x - 1 >= 0:
            pygame.draw.circle(screen,  circle.second_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1)- counter_animate, SIZE_CELL//2 + SIZE_CELL*(circle.y+1)), (SIZE_CELL*0.7)//2)
            pygame.draw.circle(screen,  circle.main_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1)- counter_animate, SIZE_CELL//2 + SIZE_CELL*(circle.y+1)), (SIZE_CELL*0.6)//2)

        if circle.y + 1 < NUM_Y_CELL:
            pygame.draw.circle(screen,  circle.second_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1), SIZE_CELL//2 + SIZE_CELL*(circle.y+1) + counter_animate), (SIZE_CELL*0.7)//2)
            pygame.draw.circle(screen,  circle.main_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1), SIZE_CELL//2 + SIZE_CELL*(circle.y+1) + counter_animate), (SIZE_CELL*0.6)//2)
        
        if circle.y -1 >= 0:
            pygame.draw.circle(screen,  circle.second_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1), SIZE_CELL//2 + SIZE_CELL*(circle.y+1)- counter_animate), (SIZE_CELL*0.7)//2)
            pygame.draw.circle(screen,  circle.main_color,  (SIZE_CELL//2 + SIZE_CELL*(circle.x+1), SIZE_CELL//2 + SIZE_CELL*(circle.y+1)- counter_animate), (SIZE_CELL*0.6)//2)
            

        
