from binary_heap import BinaryHeap
from node import Node
import time

class EarlyAstar:
    def __init__(self, initial_state, heuristic, weight=1):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        self.heuristic = heuristic
        self.solution = None
        self.U = float('inf')  # Valor de U inicial (infinito)

    def search(self):
        self.start_time = time.process_time()
        '''
        COMPLETAR
        '''
        # Para hacer este código se utilizó astar como base y se consideraron algunas recomendaciones de copilot
        self.open = BinaryHeap()
        self.expansions = 0
        self.solution = None

        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)

        initial_node.key = self.weight*initial_node.h  # asignamos el valor f
        self.open.insert(initial_node)

        # Almacenar los nodos generados
        self.generated = {}

        while not self.open.is_empty():
            actual_node = self.open.extract()

            if self.U <= actual_node.key:
                self.solution = actual_node
                self.end_time = time.process_time()
                return self.solution

            succ = actual_node.state.successors()
            self.expansions += 1

            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None
                path_cost = actual_node.g + cost

                if child_node and path_cost >= child_node.g:
                    continue

                if not child_node:
                    child_node = Node(child_state)
                    child_node.h = self.heuristic(child_state)
                    self.generated[child_state] = child_node

                child_node.g = path_cost
                child_node.parent = actual_node
                child_node.action = action
                child_node.key = child_node.g + self.weight*child_node.h

                if child_state.is_goal() and child_node.g < self.U:
                    self.U = child_node.g
                    self.solution = child_node

                if child_node.key <= self.U:
                    if child_node.heap_index == 0:
                        self.open.insert(child_node)
                    else:
                        self.open.percolateupordown(child_node.heap_index, child_node)

                            
        self.end_time = time.process_time()
        return None