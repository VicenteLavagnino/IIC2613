import math


class LCell:
    def __init__(self, x, y, p, map):
        self.x = x
        self.y = y
        self.p = p 
        self.map = map
        self.sandCost = 1
        self.iceCost = -0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.map == other.map

    def __repr__(self):
        return str((self.x, self.y, self.p))

    def __str__(self):
        return str((self.x, self.y, self.p))

    def __hash__(self):
        return hash((self.x, self.y, self.p))
    
    def successors(self):
        succ = []
        current_x, current_y = self.x, self.y  # Pre-calcula los valores de la posición actual
        current_pose = self.p

        for old_pose, new_pose, endx, endy, cost, new_move in self.map.neighbors:
            '''
            COMPLETAR
            
            No es necesario que le pongas un nombre de acción distinta a cada movimiento.
            Por lo que puedes dejar la acción como un string "move"
            '''

            # Calcula la nueva posición y el costo de la acción
            new_x = current_x + endx
            new_y = current_y + endy

            # Si la nueva posición es válida o si la nueva posición no esta visible
            if not self.map.inside(new_x, new_y) or not self.map.line_of_sight(current_x, current_y, new_x, new_y) :
                continue

            final_cost = cost
            
            if self.map.sand[new_x][new_y]:
                final_cost += self.sandCost

            elif self.map.ice[new_x][new_y]:
                final_cost += self.iceCost

            succ.append((LCell(new_x, new_y, new_pose, self.map), "move", final_cost))


        return succ

    def is_goal(self):
        return self.x == self.map.goal_x and self.y == self.map.goal_y
