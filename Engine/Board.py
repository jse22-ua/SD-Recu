import random
from personaje import Personaje
from exceptions.tooManyPlayersException import TooManyPlayersException
from exceptions.InvalidCoordinateException import InvalidCoordinateException
from npc import NPC
from player import Player

directions = {
    'q': (-1, -1),  # Arriba-izquierda(q)
    'w': (-1, 0),  # Arriba(w)
    'e': (-1, 1),  # Arriba-derecha(e)
    'a': (0, -1),  # izquierda(a)
    'd': (0, 1),  # derecha(d)
    'z': (1, -1),  # abajo-izquierda(z)
    's': (1, 0),  # abajo(s)
    'x': (1, 1),  # abajo-derecha(x)
}


class Board:
    def __init__(self, rows: int, cols: int, max_players: int, cities: list):
        self.set_cols(cols)
        self.set_rows(rows)
        self.max_players = max_players
        self.cities = cities
        self.n_players = 0
        self.squares = self.fill_squares(rows, cols)  # casillas

    def set_rows(self, rows: int):
        if rows <= 0:
            raise Exception('Invalid max of rows')
        self.rows = rows

    def set_cols(self, cols: int):
        if cols <= 0:
            raise Exception('Invalid max of cols')
        self.cols = cols

    def fill_squares(self,rows, cols):
        squares = []
        for i in range(rows):
            row = []
            for j in range(cols):
                x = random.randint(1, 100)
                if x <= 10:
                    row.append("M")
                elif x > 10 and x <= 40:
                    row.append("A")
                else:
                    row.append(None)
            squares.append(row)
        return squares

    def get_temperatura(self, x, y):
        if x < 0 or x > self.rows-1 or y < 0 or y > self.cols-1:
            raise InvalidCoordinateException(x, y)
        x_cond = x < self.rows/2
        y_cond = y < self.cols/2
        if x_cond and y_cond:
            return self.cities[0][1]
        elif y_cond:
            return self.cities[1][1]
        elif x_cond:
            return self.cities[2][1]
        else:
            return self.cities[3][1]

    def get_square(self, row, cols):
        return self.squares[row][cols]
    
    def get_Coord(self,id_player):
        for i in range(self.rows):
            for j in range(self.cols):
                if isinstance(self.squares[i][j],Personaje):
                    if self.squares[i][j].id == id_player:
                        return self.squares[i][j]

    def addPlayerC(self,x:int,y:int, player: Personaje):
        if int(self.n_players) == int(self.max_players):
            raise TooManyPlayersException(self.n_players)

        self.squares[x][y] = player
        player.set_position(x, y)
        if isinstance(player,Player):
            self.n_players += 1

    def addPlayer(self, player: Personaje):
        if int(self.n_players) == int(self.max_players):
            raise TooManyPlayersException(self.n_players)

        while True:
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.cols-1)
            if not isinstance((self.squares[x][y]), Personaje):
                break
        self.squares[x][y] = player
        player.set_position(x, y)
        if isinstance(player,Player):
            self.n_players += 1

    
    def get_nextPosition(self,x,y,direction):
        dx, dy = directions[direction]
        new_x = x + dx
        new_y = y + dy

        if new_x < 0:
            new_x = self.rows-1
        elif new_x >= self.rows:
            new_x = 0

        if new_y < 0:
            new_y = self.cols-1
        elif new_y >= self.cols:
            new_y = 0
        
        return (new_x,new_y)

    def fight(self,enemy:Personaje,player:Personaje)->bool:
        temperatura = self.get_temperatura(enemy.position_x,enemy.position_y)
        if enemy.calculate_nivel(temperatura) < player.calculate_nivel(temperatura):
            enemy.die()
            print(f"{player.getSymbol()}: gano a {enemy.getSymbol()}")
            self.n_players -= 1
            return True
        elif enemy.calculate_nivel(temperatura)> player.calculate_nivel(temperatura):
            self.squares[player.position_x][player.position_y] = None
            player.die()
            print(f"{enemy.getSymbol()}: gano a {player.getSymbol()}")
            self.n_players -=1
        return False
    
    def asignCoord(self,coord,player:Personaje):
        temp = self.get_temperatura(coord[0],coord[1])
        self.squares[player.position_x][player.position_y] = None
        self.squares[coord[0]][coord[1]] = player
        player.move(coord[0],coord[1],temp)
        
    def move(self,player: Personaje, direction)->bool:
        if not player.is_alive:
            raise ValueError("El jugador está muerto, no puede moverse")
        coord = self.get_nextPosition(player.position_x,player.position_y,direction)
        #print(coord)
        in_square = self.squares[coord[0]][coord[1]]
        if isinstance(in_square,Personaje):
            if self.fight(in_square,player):
                self.asignCoord(coord,player)
        elif isinstance(in_square,str): 
            if in_square == "M":
                #print(f"{player.getSymbol()} : pisó una mina")
                self.squares[player.position_x][player.position_y] = None
                player.die()
                self.n_players-=1
            else:
                self.asignCoord(coord,player)
                if isinstance(player,Player): 
                    player.catchFood()
                    #print(f"{player.getSymbol()} : pisó una alimento")
        else:   
            #print("casilla vacia")
            self.asignCoord(coord,player)
    

    def showBoard(self) -> str:  # corregir/probar/añadir ciudades
        tablero = "   "
        string1 = ""
        for aux in range(self.cols):
            string1 += f" {aux} "
        tablero += string1 + "\n" + "\n"
        for i in range(self.rows):
            tablero += f" {i}"
            if i < 10:
                tablero += " "
            for j in range(self.rows):
                if j > 9: 
                    tablero += " "
                in_square = self.squares[i][j]
                if isinstance(in_square, str):
                    tablero += f"|{in_square}|"
                elif isinstance(in_square, Personaje):
                    tablero += f"|{in_square.getSymbol()}|"
                else:
                    tablero += f"| |"
            tablero += "\n" + "\n"
        return tablero
    
    def get_winner(self):
        for i in range(self.rows):
            for j in range(self.rows):
                in_square = self.squares[i][j]
                if isinstance(in_square, Player):
                  self.winner = in_square.id
    
    