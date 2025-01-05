from copy import deepcopy
from random import shuffle

def valid_plays(circles, jugador, table_size):
    ## NO MODIFICAR
    valid_circles = []
    for list_circle in circles:
        for circle in list_circle:
            if circle.id == jugador.id or circle.id == -1:
                # espacio del jugador y vacio
                if circle.x > -1 and circle.y > -1 and circle.x < table_size[0] and circle.y < table_size[1]:
                    valid_circles.append((circle.x, circle.y))
    
    return valid_circles
    
    
def update_game(circles, x, y, jugador, table_size):
    ## NO MODIFICAR

    if not (x,y) in valid_plays(circles, jugador, table_size):
        return False
    
    circles[x][y].number += 1
    circles[x][y].id = jugador.id
    circles[x][y].update_color(jugador.color)

    return True
            

def chain_reaction(circles, list_reaction, jugador, table_size):
    ## NO MODIFICAR
    for circle in list_reaction:
        circle.number -= circle.max_number + 1
        if circle.y + 1 < table_size[1]:
            circles[circle.x][circle.y + 1].number += 1
            circles[circle.x][circle.y + 1].id = jugador.id
            circles[circle.x][circle.y + 1].update_color(jugador.color)

        if circle.x + 1 < table_size[0]:
            circles[circle.x + 1][circle.y ].number += 1
            circles[circle.x + 1][circle.y ].id = jugador.id
            circles[circle.x + 1][circle.y ].update_color(jugador.color)

        if circle.x - 1 >= 0:
            circles[circle.x - 1][circle.y].number += 1
            circles[circle.x - 1][circle.y].id = jugador.id
            circles[circle.x - 1][circle.y].update_color(jugador.color)
        
        if circle.y -1 >= 0:
            circles[circle.x][circle.y - 1].number += 1
            circles[circle.x][circle.y - 1].id = jugador.id
            circles[circle.x][circle.y - 1].update_color(jugador.color)

        if circle.number <= 0:
            circle.id = -1
def fast_chain_reaction(circles,x,y, JUGADORES, JUGADOR, table_size):
    ## NO MODIFICAR
    update_game(circles, x, y, JUGADOR, table_size)
    reaction = True
    while reaction:
        reaction, list_reaction = check_limits(circles)
        if is_winner(circles, JUGADORES):
            break
        chain_reaction(circles, list_reaction, JUGADOR, table_size)
    return circles


def get_all_moves(circles, JUGADORES, JUGADOR, table_size):
    ## NO MODIFICAR
    moves = []
    for move in valid_plays(circles, JUGADOR, table_size): 
        x, y = move
        circles_copy = deepcopy(circles)
        moves.append((fast_chain_reaction(circles_copy, x, y, JUGADORES, JUGADOR, table_size),(x,y)))
    shuffle(moves)
    return moves


def check_limits(circles):
    ## NO MODIFICAR
    temp_bool = False
    list_reaction = []
    for list_circle in circles:
        for circle in list_circle:
            if (circle.max_number < circle.number):
                temp_bool = True
                list_reaction.append(circle)
            
    return temp_bool, list_reaction


def is_winner(circles, lista_jugadores):
        ## NO MODIFICAR
    for jugador in lista_jugadores:
        if not jugador.ya_jugo:
            return False
    jugadores = set()
    ganador = -1
    for list_circle in circles:
        for circle in list_circle:
            if circle.id != -1:
                jugadores.add(circle.id)
                ganador = circle.id
            if len(jugadores) > 1:
                return False
    return True
