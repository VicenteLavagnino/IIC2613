class Circle():
    ## NO MODIFICAR
    def __init__(self, x, y, number, id, table_size):
        # id -1 si no tiene jugador asignado
        self.x = x
        self.y = y
        self.number = number
        self.id = id
        self.color = (0,0,0)
        self.second_color = (0,0,0)
        self.main_color = (0,0,0)
        self.table_size = table_size
        self.detect_max_number()

    def update_color(self, color):
        self.color = color 
        GREEN = (0, 220, 0)
        DARK_GREEN = (0, 170, 0)
        LIGHT_GREEN = (0, 255, 0)
        RED = (220, 0, 0)
        DARK_RED = (170, 0, 0)
        LIGHT_RED = (255, 0, 0)
        YELLOW = (255,255,0)
        if self.color == RED:
            self.main_color = LIGHT_RED
            self.second_color = RED
        elif self.color == GREEN:
            self.main_color = LIGHT_GREEN
            self.second_color = GREEN
        if self.number == self.max_number:
            self.second_color = YELLOW
    
    
    def detect_max_number(self):
        self.max_number = 3
        if self.x == 0 or self.x == self.table_size[0]-1:
            self.max_number -= 1
        
        if self.y == 0 or self.y == self.table_size[1]-1:
            self.max_number -= 1