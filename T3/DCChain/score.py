def score_circle_amount(circles, JUGADOR):
    contador_j1 = 0
    contador_j2 = 0
    resta = 0
    for list_circle in circles:
        for circle in list_circle:
            if circle.id == 0:
                contador_j1 += 1

            elif circle.id == 1:
                contador_j2 += 1
    if JUGADOR.id == 0:
        resta = contador_j1 - contador_j2
    else:
        resta = contador_j2 - contador_j1
    
    return resta


def score_circle_values(circles, JUGADOR):
    contador_j1 = 0
    contador_j2 = 0
    resta = 0
    for list_circle in circles:
        for circle in list_circle:
            if circle.id == 0:
                contador_j1 += circle.number

            elif circle.id == 1:
                contador_j2 += circle.number
    if JUGADOR.id == 0:
        resta = contador_j1 - contador_j2
    else:
        resta = contador_j2 - contador_j1
    
    return resta


## AGREGAR AQUÍ TUS FUNCIONES DE EVALUACIÓN
def score_circle_amount_2(circles, JUGADOR):
    contador_j1 = 0
    contador_j2 = 0
    resta = 0
    for list_circle in circles:
        for circle in list_circle:
            if circle.id == 0:
                contador_j1 += 0.5

            elif circle.id == 1:
                contador_j2 += 0.5
    if JUGADOR.id == 0:
        resta = contador_j1 - contador_j2
    else:
        resta = contador_j2 - contador_j1
    
    return resta