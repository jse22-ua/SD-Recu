
from personaje import Personaje

class Player(Personaje):
    def __init__(self, id:int,alias:str,EF:int,EC:int,nivel:int):
        super().__init__(id,nivel)
        self.alias = alias
        self.EF = EF
        self.EC = EC


    def getSymbol(self):
        return "" + self.alias[0] + str(self.id)
    
    def calculate_nivel(self,temperature)->int:
        nivel = 0
        if temperature <= 10:
            nivel = self.nivel + self.EF
        elif temperature >= 25:
            nivel = self.nivel + self.EC
        if nivel<0:
            nivel = 0
        print(self.alias)
        print(nivel)
        return nivel
    
    def move(self,x,y,temperature):
        super().move(x,y,temperature)
        self.nivel = self.calculate_nivel(temperature)

    def catchFood(self):
        self.nivel += 1

