import random
from Character import Character
from Exceptions.TooManyPlayersException import TooManyPlayersException
from NPC import NPC
from Player import Player


class Board:
    def __init__(self, rows, cols, max_players):
        self.rows = rows
        self.cols = cols
        self.max_players = max_players
        self.n_players = 0
        self.squares = []  # casillas
        for i in range(rows):
            row = []
            for j in range(cols):
                x = random.randint(1, 100)
                if x <= 20:
                    row.append("M")
                elif x > 20 and x <= 50:
                    row.append("A")
                else:
                    row.append(None)
            self.squares.append(row)


    def get_square(self, row, cols):
        return self.squares[row][cols]

    def addPlayer(self, player):
        if self.n_players == self.max_players:
            raise TooManyPlayersException(self.n_players)
        
        while True:
            x = random.randint(0, self.rows)
            y = random.randint(0, self.cols)
            if isinstance((self.squares[x][y]), Character):
                break
            self.squares[x][y] = player

    def showBoard(self):#corregir/probar
        tablero = "   "
        for aux in range(self.cols):
            string1 =+ f" {aux} " 
        tablero = string1 + "\n" + " - " * self.cols
        for i in range(self.rows):
            tablero =+ f"{i} |"
            for j in range(self.rows):
                if isinstance(self.squares[i][j],str):
                    tablero =+ f"| {self.squares[i][j]} |"
                elif isinstance(self.squares[i],[j],NPC):
                    tablero =+ f"| {self.squares[i][j].nivel} |"
                elif isinstance(self.squares[i],[j],Player):
                    tablero =+ f"| {self.squares[i][j].getSymbol()} |"
                else:
                    tablero =+ f"|    |"
            tablero =+ " - " * self.cols
        return tablero
