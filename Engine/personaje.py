class Personaje:
    def __init__(self,id:int,nivel:int):
        self.nivel = nivel
        self.id = id
        self.is_alive = True

    def set_position(self,x:int,y:int):
        self.position_x = x
        self.position_y = y
    
    def die(self):
        self.is_alive = False
        self.position_x = None
        self.position_y = None
    
    def calculate_nivel(self,temperature)->int:
        return self.nivel

    def getSymbol(self):
        return f"{self.nivel}"

    def move(self,x,y,temperature):
        self.set_position(x,y)