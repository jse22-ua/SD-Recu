class TooManyPlayersException(Exception):
    def __init__(self, players):
        self.players = players
    
    def getError(self):
        return f"Se supero el numero máximo de jugadores: {self.players}"