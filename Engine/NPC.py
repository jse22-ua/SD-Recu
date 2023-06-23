from .personaje import Personaje

class NPC(Personaje):
    def __init__(self,id,nivel):
        super().__init__(id,nivel)

