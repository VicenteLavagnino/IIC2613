from Game.Player import Player
import pygame
from Game.Circle import Circle
from Game.Front import update_screen, key_press
from Game.Board import update_game, chain_reaction, check_limits, is_winner, valid_plays
from minimax import minimax
import random
import time

## ACÁ IMPORTAR NUEVAS FUNCIONES DE EVALUACIÓN
from score import score_circle_amount, score_circle_values, score_circle_amount_2

def show_screen(screen, circles, JUGADOR, SIZE_CELL, NUM_X_CELL, NUM_Y_CELL, X_MAX, Y_MAX, counter_animate = 0, list_reaction = []):
    update_screen(screen, circles, JUGADOR, SIZE_CELL, NUM_X_CELL, NUM_Y_CELL, X_MAX, Y_MAX, counter_animate, list_reaction)
    pygame.display.update()
    pygame.display.flip()

if __name__ == '__main__':

    ## ASPECTOS DE JUEGO
    ## COLORES 
    GREEN = (0, 220, 0)
    LIGHT_GREEN = (0, 255, 0)
    BLACK = (0,0,0)
    RED = (220, 0, 0)
    LIGHT_RED = (255, 0, 0)
    BLUE = (0, 0, 128)  

    ## Tiempo de transiciones, si no quieres ver las transiciones, igualalo a 0.0
    sleep_time = 1.0

    ## True si se quiere ver la animación
    ANIMACION = False

    ## Tamaño celda animación
    SIZE_CELL = 100
    ANIMATE_SKIP = (SIZE_CELL**2)//(50**2)

    ## Tamaño tablero
    NUM_X_CELL = 5
    NUM_Y_CELL = 5

    ## PARAMETROS MINIMAX
    DEPTH_J1 = 1 # PROFUNDIDAD JUGADOR 1
    DEPTH_J2 = 1 # PROFUNDIDAD JUGADOR 2

    ## True si se quiere implementar la Poda Alpha-Beta
    ALPHABETA = True # PODA ALPHA-BETA

    ## PARAMETROS JUGADORES
    ## "MINIMAX" , "HUMANO" , "RANDOM"
    ## JUGADOR_ID = Player(TIPO JUGADOR, COLOR, ID, DEPTH, función de evaluación)
    ## NO MODIFICAR: ID
    ## MODIFICAR: TIPO JUGADOR, DEPTH, función de evaluación
    JUGADOR_1 = Player("MINIMAX", RED, 0, DEPTH_J1, eval_func=score_circle_amount)
    JUGADOR_2 = Player("MINIMAX", GREEN, 1, DEPTH_J2, eval_func=score_circle_amount_2)
    JUGADORES = [JUGADOR_1, JUGADOR_2]

    ## TAMAÑO PANTALLA
    X_MAX = SIZE_CELL*(NUM_X_CELL+2)
    Y_MAX = SIZE_CELL*(NUM_Y_CELL+2)
   

    ## Si hay jugador HUMANO, tiene que haber ANIMACION
    if JUGADOR_1.tipo == "HUMANO" or JUGADOR_2.tipo == "HUMANO":
        ANIMACION = True

    ## INICIO DE PYGAME
    ## NO MODIFICAR
    if ANIMACION:
        pygame.init()
        pygame.key.set_repeat(1,50)

        ## CREACIÓN DE VENTANA
        screen = pygame.display.set_mode((X_MAX,Y_MAX))
        pygame.display.set_caption('Chain Reaction')

    ## GENERAR JUEGO TABLERO
    circles = []
    for x_pos in range(NUM_X_CELL):
        temp_circles=[]
        for y_pos in range(NUM_Y_CELL):
            temp_circles.append(Circle(x_pos, y_pos, 0, -1, (NUM_X_CELL,NUM_Y_CELL)))
        circles.append(temp_circles)
    
    JUGADA = 0
    
    tiempos_J1 = []
    tiempos_J2 = []
    jugadas = 0
    while True:
        ## JUGAR
        ## NO MODIFICAR
        
        JUGADOR = JUGADORES[JUGADA]
        
        start_time = time.time()
        if JUGADOR.tipo == "HUMANO":
            while not key_press():
                show_screen(screen, circles, JUGADOR, SIZE_CELL, NUM_X_CELL, NUM_Y_CELL, X_MAX, Y_MAX)
            x,y= pygame.mouse.get_pos()
            x, y = x//SIZE_CELL - 1, y//SIZE_CELL - 1
            
            
        elif JUGADOR.tipo == "RANDOM": 
            find = False
            while not find:
                x,y = random.randint(0, NUM_X_CELL), random.randint(0, NUM_Y_CELL)
                if (x,y) in valid_plays(circles, JUGADOR, (NUM_X_CELL,NUM_Y_CELL)):
                    find = True
        
        elif JUGADOR.tipo == "MINIMAX": 
            result = minimax(circles, JUGADORES, JUGADOR, JUGADOR.id, (NUM_X_CELL,NUM_Y_CELL), JUGADOR.depth, True, alphabeta=ALPHABETA, eval_func = JUGADOR.eval_func)
            x,y = result[1]
        end_time = time.time()
        jugadas += 1
        execution_time = end_time - start_time
        
        string = f"El algoritmo {JUGADOR.tipo}, Jugador {JUGADOR.id+1}, "
        if JUGADOR.tipo == "MINIMAX":
            string += f"de profundidad {JUGADOR.depth}, "
        
        string += f"tardo {round(execution_time,3)}"
        
        #print(string)

        if JUGADOR.id == 0:
            tiempos_J1.append(execution_time)
        elif JUGADOR.id == 1:
            tiempos_J2.append(execution_time)
    
        status = update_game(circles, x, y, JUGADOR, (NUM_X_CELL,NUM_Y_CELL))
        
        if status:
            reaction = True
            while reaction:
                reaction, list_reaction = check_limits(circles)
                if is_winner(circles, JUGADORES):
                    break
                if ANIMACION:
                    counter_animate = 0
                    while counter_animate <= SIZE_CELL:
                        counter_animate += ANIMATE_SKIP
                        show_screen(screen, circles, JUGADOR, SIZE_CELL, NUM_X_CELL, NUM_Y_CELL, X_MAX, Y_MAX, counter_animate, list_reaction)
                
                chain_reaction(circles, list_reaction, JUGADOR, (NUM_X_CELL,NUM_Y_CELL))
            
            JUGADOR.ya_jugo = True
            if not JUGADA:
                JUGADA = 1
            else:
                JUGADA = 0
        
        if ANIMACION:
            ## ACTUALIZACION DE PYGAME
            show_screen(screen, circles, JUGADOR, SIZE_CELL, NUM_X_CELL, NUM_Y_CELL, X_MAX, Y_MAX)
        
        ## IMPRIMIR RESULTADOS
        if is_winner(circles, JUGADORES):
            ## se resetea el atributo ya_jugo para poder realizar muchas jugadas
            for jugador in JUGADORES:
                jugador.ya_jugo = False
            print(f"Jugador {JUGADOR.id + 1} es el ganador")
            print(f"Jugador 1 tardo en promedio {round(sum(tiempos_J1)/len(tiempos_J1),3)} por jugada y en total {round(sum(tiempos_J1),2)}")
            print(f"Jugador 2 tardo en promedio {round(sum(tiempos_J2)/len(tiempos_J2),3)} por jugada y en total {round(sum(tiempos_J2),2)}")
            print(f"La partida tomo {jugadas} Jugadas en total (Ambos jugadores)")
            break
        