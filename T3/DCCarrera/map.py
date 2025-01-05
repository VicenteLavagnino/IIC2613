from termcolor import colored
import numpy as np
import math

class Map:
    diag_cost = math.sqrt(2)  ## la definimos como constante para evitar computarla multiples veces
    def __init__(self, epsilon, filename='map.txt'):
        self.neighbors = []
        self.actions = []
        self.costs = []
        self.connectivity = 4
        self.epsilon = epsilon
        file = open(filename, 'r')
        lines = file.readlines()
        dimensions = [int(x) for x in lines[0].split(',')]
        self.size_x = dimensions[0]
        self.size_y = dimensions[1]
        self.map = []
        self.sand = []
        self.ice = []
        for x in range(0, self.size_x):
            self.map.append([False]*self.size_y)
            self.sand.append([False]*self.size_y)
            self.ice.append([False]*self.size_y)
            
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                c = lines[1+y][x]
                if c == '.' or c == 'H' or c == 'A':
                    self.map[x][y] = True
                elif c == '@':
                    self.map[x][y] = False
                elif c == 'I':
                    self.map[x][y] = True
                    self.init_x = x
                    self.init_y = y
                elif c == 'G':
                    self.map[x][y] = True
                    self.goal_x = x
                    self.goal_y = y
                # Revisar los terrenos
                if c == 'H':
                    self.ice[x][y] = True
                elif c == 'A':
                    self.sand[x][y] = True

    
    def rotation_matrix_2d(self, theta):
        rotation = np.array([
                [np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)]
            ])
        rotation = np.where(np.abs(rotation) < 1e-5, 0, rotation)
        return rotation

    def floor_ceil(self, vector, tolerance=1e-5):
        return np.where(np.abs(vector) < tolerance, 0,
                        np.where(vector >= 0, np.floor(vector), np.ceil(vector)))
    
    def ceil_floor(self, vector, tolerance=1e-5):
        return np.where(np.abs(vector) < tolerance, 0,  
                        np.where(vector >= 0, np.ceil(vector), np.floor(vector)))
    
    def generate_primitive_neighbor(self, initialPose, numberOldPose, initialMove, relativePosition, rotations, k, cost):
        old_pose = self.ceil_floor(initialPose @ self.rotation_matrix_2d(rotations[k])).astype(int)
        old_pose = (old_pose[0], old_pose[1])
        new_pose = self.ceil_floor(initialPose @ self.rotation_matrix_2d(rotations[k]-(numberOldPose/4)*np.pi)).astype(int)
        new_pose = (new_pose[0], new_pose[1])
        end = self.floor_ceil(initialMove @ self.rotation_matrix_2d(rotations[k])).astype(int)
        new_move_rotated = self.floor_ceil(relativePosition @ self.rotation_matrix_2d(rotations[k])).astype(int)
        new_move_rounded = [tuple(vector) for vector in new_move_rotated]
        return (old_pose, new_pose, end[0], end[1], cost, new_move_rounded)

    def set_connectivity(self, n):
        '''
        Esta función recibe n que es la conectividad a utilizar y configura las conexiones.

        Conectividades simples -> Estos se pueden llamar 
        n = 4 : Conexione Norte, Sur, Este, Oeste
        n = 8 : Conexione Norte, Sur, Este, Oeste y las diagonales

        Primitivas -> Estos NO se pueden llamar (no puede moverse libremente)
        n = "primitiveStraight" : Carga los movimientos rectos de las primitivas
        n = "primitiveDiagonal" : Carga los movimientos en diagonal de las primitivas
        n = "primitiveRightAngle" : Carga los movimientos curvilineos en angulo Pi/2
        n = "primitiveDiagonalAngle" : Carga los movimientos curvilineos en ángulo Pi/4

        Conjuntos de primitivas -> Estos se pueden llamar 
        n = "primitiveSimpleRight" : Carga los movimientos rectos y curvilineos en pi/2
        n = "primitiveSimpleDiagonal" : Carga los movimientos rectos, diagonales y curvilineos en pi/4
        n = "primitiveFull" : Carga todas las primitivas
        '''

        actions4 = ['e', 'w', 's', 'n']
        actions8 = ['ne', 'nw', 'se', 'sw']

        if n == 4:
            self.neighbors = [(1,0), (-1,0), (0,1), (0,-1)]
            self.costs     = [1]*4
            self.actions   = actions4
        elif n == 8:
            '''
            COMPLETAR
            '''
            self.neighbors = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
            # costo de diagonales es raiz de 2 y de los otros es 1 
            self.costs     = [1, 1, 1, 1, math.sqrt(2), math.sqrt(2), math.sqrt(2), math.sqrt(2)]
            self.actions   =  actions4 + actions8


        elif n == "primitiveStraight":
            '''
            COMPLETAR
            '''
            cost = 1
            initialPose = np.array([0, 1], dtype = int)
            rotations = [(1/4)*np.pi,(2/4)*np.pi,(3/4)*np.pi,(4/4)*np.pi,(5/4)*np.pi,(6/4)*np.pi,(7/4)*np.pi,(8/4)*np.pi]

            numberOldPose = 0 #0 grados
            relativePosition = np.array([[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]])
            initialMove = np.array([0, 5], dtype = int)

            for k in range(len(rotations)):
                neighbor = self.generate_primitive_neighbor(initialPose, numberOldPose, initialMove, relativePosition, rotations, k, cost)
                self.neighbors.append(neighbor)
                self.costs.append(cost)

        elif n == "primitiveRightAngle":
            cost = 2.5*math.pi + self.epsilon
            initialPose = np.array([0, 1], dtype = int)
            rotations = [(1/4)*np.pi,(2/4)*np.pi,(3/4)*np.pi,(4/4)*np.pi,(5/4)*np.pi,(6/4)*np.pi,(7/4)*np.pi,(8/4)*np.pi]
            
            numberOldPose = 2 #+90 grados
            relativePosition = np.array([[0, 1], [0, 2], [-1, 3], [-1, 4], [-2, 4], [-3, 5], [-4, 5], [-5, 5]])
            initialMove = np.array([-5, 5], dtype = int)

            for k in range(len(rotations)):
                neighbor = self.generate_primitive_neighbor(initialPose,
                                                            numberOldPose, initialMove, relativePosition, rotations, k, cost)
                self.neighbors.append(neighbor)
                self.costs.append(cost)

            # Movimientos curvos rectos en sentido horario
            numberOldPose = -2 #-90 grados
            relativePosition = np.array([[0, 1], [0, 2], [1, 3], [1, 4], [2, 4], [3, 5], [4, 5], [5, 5]])
            initialMove = np.array([5, 5], dtype = int)

            for k in range(len(rotations)):
                neighbor = self.generate_primitive_neighbor(initialPose,
                                                            numberOldPose, initialMove, relativePosition, rotations, k, cost)
                self.neighbors.append(neighbor)
                self.costs.append(cost)

        elif n == "primitiveDiagonal":
            '''
            COMPLETAR
            '''
            cost = math.sqrt(2)
            initialPose = np.array([0, 1], dtype = int)
            numberOldPose = 0 #0 grados
            rotations = [(1/4)*np.pi,(2/4)*np.pi,(3/4)*np.pi,(4/4)*np.pi,(5/4)*np.pi,(6/4)*np.pi,(7/4)*np.pi,(8/4)*np.pi]

            numberOldPose = 0 #0 grados
            relativePosition = np.array([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]])
            initialMove = np.array([4, 5], dtype = int)

            for k in range(len(rotations)):
                neighbor = self.generate_primitive_neighbor(initialPose, numberOldPose, initialMove, relativePosition, rotations, k, cost)
                self.neighbors.append(neighbor)
                self.costs.append(cost)



        elif n == "primitiveDiagonalAngle":
            # Movimientos curvos 45 grados en sentido antihorario
            cost = 4.88414 + 2*self.epsilon
            initialPose = np.array([0, 1], dtype = int)
            numberOldPose = 1 # +45 grados
            rotations = [(1/4)*np.pi,(2/4)*np.pi,(3/4)*np.pi,(4/4)*np.pi,(5/4)*np.pi,(6/4)*np.pi,(7/4)*np.pi,(8/4)*np.pi]

            relativePosition = np.array([[0, 1], [0, 2], [-1, 2], [-1, 3],[-2, 3]])
            initialMove = np.array([-2, 3], dtype = int)

            for k in range(len(rotations)):
                neighbor = self.generate_primitive_neighbor(initialPose,
                                                            numberOldPose, initialMove, relativePosition, rotations, k, cost)
                self.neighbors.append(neighbor)
                self.costs.append(cost)

            # Movimientos curvos 45 grados en sentido antihorario
            numberOldPose = -1 # -45 grados
            relativePosition = np.array([[0, 1], [0, 2], [1, 2], [1, 3],[2, 3]])
            initialMove = np.array([2, 3], dtype = int)

            for k in range(len(rotations)):
                neighbor = self.generate_primitive_neighbor(initialPose, 
                                                            numberOldPose, initialMove, relativePosition, rotations, k, cost)
                self.neighbors.append(neighbor)
                self.costs.append(cost)

        elif n == "primitiveSimpleRight":
            self.set_connectivity("primitiveStraight")
            self.set_connectivity("primitiveRightAngle")
        elif n == "primitiveSimpleDiagonal":
            self.set_connectivity("primitiveStraight")
            self.set_connectivity("primitiveDiagonal")
            self.set_connectivity("primitiveDiagonalAngle")
        elif n == "primitiveFull":
            self.set_connectivity("primitiveStraight")
            self.set_connectivity("primitiveRightAngle")
            self.set_connectivity("primitiveDiagonal")
            self.set_connectivity("primitiveDiagonalAngle")
        else:
            print("conectividad no soportada, usando conectividad 4")
            self.set_connectivity(4)

    def inside(self, x, y):
        return x >= 0 and x < self.size_x and \
               y >= 0 and y < self.size_y

    def free(self, x, y):
        return self.map[x][y]

    def obstacle(self, x, y):
        return not self.map[x][y]

    def manhattan(x1, y1, x2, y2):
        '''
        COMPLETAR
        '''
        return abs(x1 - x2) + abs(y1 - y2)

    def euclidian(x1, y1, x2, y2):
        '''
        COMPLETAR
        '''
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def octile(x1, y1, x2, y2):
        '''
        COMPLETAR
        '''
        # fórmula de la distancia octile
        # f(x, y) = max(|x1 - x2|, |y1 - y2|) + (sqrt(2) - 1) * min(|x1 - x2|, |y1 - y2|)
        # http://www.gameaipro.com/GameAIPro/GameAIPro_Chapter17_Pathfinding_Architecture_Optimizations.pdf
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

    def line_of_sight(self, x0, y0, x1, y1):  # retorna verdadero si las celdas entre (x0, y0) y (x1,y1) están libres
        dx = abs(x1-x0)                       # basado en el algoritmo de la línea de Bresenham
        dy = abs(y1-y0)                       # fuente: http://floppsie.comp.glam.ac.uk/Southwales/gaius/gametools/6.html
        if x0 < x1:
            sx = 1
        else:
            sx = -1
        if y0 < y1:
            sy = 1
        else:
            sy = -1
        err = dx-dy
        while True:
            if not self.map[x0][y0]:
                return False
            if x0 == x1 and y0 == y1:
                return True
            e2 = 2*err
            if e2 > -dy:
                err = err - dy
                x0 = x0 + sx
            if e2 < dx:
                err = err + dx
                y0 = y0 + sy

    def draw_solution(self, trace, generated_positions=[], primitives = True):
        if primitives:
          for i in range(len(trace)):
              trace[i] = (trace[i][0], trace[i][1])
                
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                if x == self.init_x and y == self.init_y:
                    print('I', end='')
                elif x == self.goal_x and y == self.goal_y:
                    print('G', end='')
                elif self.ice[x][y] == True:
                    print(colored('*', 'cyan'), end='')
                elif self.sand[x][y] == True:
                    print(colored('*', 'yellow'), end='')
                elif (x, y) in trace:
                    print(colored('*', 'green'), end='')
                elif (x, y) in generated_positions:
                    print(colored('X', 'red'), end='')
                elif self.map[x][y] == True:
                    print('.', end='')
                elif self.map[x][y] == False:
                    print(colored('@', 'white'), end='')
            print('')