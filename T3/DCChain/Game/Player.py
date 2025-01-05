class Player:
    def __init__(self, tipo, color, id, depth, eval_func):
        ## NO MODIFICAR
        self.tipo = tipo
        self.color = color
        self.id = id
        self.ya_jugo = False
        self.depth = depth
        self.eval_func = eval_func

