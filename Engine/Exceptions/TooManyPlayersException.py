class TooManyPlayersException(Exception):
    def __init__(self, players):
        self.players = players
    
    def getError(self):
        return f"ERROR: Se supero el numero máximo de jugadores: {self.players}"