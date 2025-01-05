import math

class Cell:
    def __init__(self, x, y, map):
        self.x = x
        self.y = y
        self.map = map
        self.sandCost = 1
        self.iceCost = -0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.map == other.map

    def __repr__(self):
        return str((self.x, self.y))

    def __str__(self):
        return str((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def successors(self):
        succ = []

        for d, a, cost in zip(self.map.neighbors, self.map.actions, self.map.costs):
            dx, dy = d
            newx, newy = self.x+dx, self.y+dy
            if self.map.inside(newx, newy) and self.map.line_of_sight(self.x, self.y, newx, newy):
                
                # Revisar si el camino tiene algún costo extra o algún acelerador
                sand = self.map.sand
                ice = self.map.ice
                if sand[newx][newy]:
                    cost += self.sandCost
                elif ice[newx][newy]:
                    cost += self.iceCost
                succ.append((Cell(newx, newy, self.map), a, cost))

        return succ

    def is_goal(self):
        return self.x == self.map.goal_x and self.y == self.map.goal_y
