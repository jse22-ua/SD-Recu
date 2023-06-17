from Character import Character

class Player(Character):
    def __init__(self, id,alias,EF,EC):
        super().__init__(id)
        self.alias = alias
        self.EF = EF
        self.EC = EC

    def getSymbol(self):
        return "" + self.alias[0] + self.nivel

        
