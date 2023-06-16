'''    N
       ^
   W <-|-> E
       v
       S
'''
directions = {
    'q' : (-1, -1),  # Arriba-izquierda(q)
    'w' : (0, -1),  # Arriba(w)
    'e' : (1, -1),  # Arriba-derecha(e)
    'a' : (-1, 0),  # izquierda(a)
    'd' : (1, 0),  # derecha(d)
    'z' : (-1, 1),  # abajo-izquierda(z)
    's' : (0, 1),  # abajo(s)
    'x' : (1, 1),  # abajo-derecha(x)
}

rows_max = 20
cols_max = 20


class Coordinate:
    def __init__(self, x, y):
        if (x < 1 or x > rows_max or y < 1 or y > rows_max):
            raise ValueError("Coordenada incorrecta")
        self.x = x
        self.y = y

    def moveCoord(self, direction):
        dx,dy = directions[direction]
        new_x = self.x + dx
        new_y = self.y + dy

        if new_x < 1:
            new_x = 20
        elif new_x > 20:
            new_x = 1

        if new_y < 1:
            new_y = 20
        elif new_y > 20:
            new_y = 1
        self.x = new_x
        self.y = new_y

    def __str__(self):
        return f"({self.x},{self.y})"
    
    def 

c1 = Coordinate(1,2)
c2 = Coordinate(20,20)
c3 = Coordinate(2,3)

c1.moveCoord(0) # (20,2)
c2.moveCoord(7) #(1,1)
c3.moveCoord(1) #(2,2)

print(c1)
print(c2)
print(c3)