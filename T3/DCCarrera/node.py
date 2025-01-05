class Node:
    def __init__(self, search_state):
        self.state = search_state
        self.parent = None
        self.action = ''        # Nombre de la accion
        self.key = -1           # Función f
        self.g = 10000000000    # Función g de A*
        self.heap_index = 0     # la posición de este nodo en el heap de Open (0 si es que no está en el heap)
        self.h = -1             # Resultado de la función h de A*
        self.closed = False     # Usado para A*. True si el nodo está closed

    def __repr__(self):
        return self.state.__repr__()

    def trace(self):
        trace = []
        n = self
        while n:
            trace.insert(0, n.state)
            n = n.parent
        return trace

    def print_trace(self):
        s = ''
        if self.parent:
            s = self.parent.trace()
            s += '-' + self.action + '->'
        s += str(self.state)
        return s
