import sqlite3
import os
from Board import Board
from Exceptions.InvalidCoordinateException import InvalidCoordinateException
from NPC import NPC
from Player import Player

'''
ruta = os.path.dirname(__file__)
ruta = os.path.dirname(ruta)
ruta = ruta + '\database.db'
ruta = ruta.replace('\\', '\\\\')
'''
ruta = "../database.db"

def createMap(max_players):
    con = sqlite3.connect(ruta)
    cursor  = con.cursor()
    cursor.execute('SELECT COUNT(*) FROM mapa')
    numero_filas = cursor.fetchone()[0]
    cursor.execute("Insert into mapa (partida, max_jugadores) values(?,?)",("partida" + str(numero_filas+1),int(max_players)))
    mapa_id = cursor.lastrowid
    con.commit()
    cursor.close()
    con.close()
    return mapa_id

def asignarArea(x,y,max_x=20,max_y=20):
        if x < 0 or x > max_x-1 or y < 0 or y > max_y-1:
             raise InvalidCoordinateException(x, y)
        x_cond = x < max_x/2
        y_cond = y < max_y/2
        if x_cond and y_cond:
            return 0
        elif y_cond:
            return 1
        elif x_cond:
            return 2
        else:
            return 3

def saveBoard(tablero:Board,cities):
    con = sqlite3.connect(ruta)
    cursor  = con.cursor()
    mapa_id = createMap(tablero.max_players)
    for city in cities:
        cursor.execute("Insert into ciudades_mapa(id_mapa,id_ciudad) values(?,?)",(mapa_id,city))
    for i in range(tablero.rows):
        for j in range(tablero.cols):
            if tablero.squares[i][j] == None:
                cursor.execute("Insert into casilla(x,y,ciudad,id_mapa) values(?,?,?,?)",(i,j,cities[asignarArea(i,j)],mapa_id))
            else:
                cursor.execute("Insert into casilla(x,y,contenido,ciudad,id_mapa) values(?,?,?,?,?)",(i,j,tablero.squares[i][j],cities[asignarArea(i,j)],mapa_id))
    con.commit()
    cursor.close()
    con.close()

    return mapa_id

def movePlayer(id_player:int,x:int,y:int):
    con = sqlite3.connect(ruta)
    cursor  = con.cursor()
    cursor.execute(f"SELECT x,y FROM casilla where personaje_id = {id_player}")
    res = cursor.fetchone()
    cursor.execute(f"UPDATE casilla SET personaje_id = {None} WHERE x = {res[0]} and y = {res[1]}")
    cursor.execute(f"UPDATE casilla SET personaje_id = {id_player} WHERE x = {x} and y = {y}")
    cursor.execute()

def saveNPC(npc:NPC):
    con = sqlite3.connect(ruta)
    cursor  = con.cursor()
    cursor.execute('SELECT COUNT(*) FROM personaje')
    numero_filas = cursor.fetchone()[0]
    cursor.execute("Insert into personaje(nivel,alias) values(?,?)",(npc.nivel,"NPC"+str(numero_filas+1)))
    id = cursor.lastrowid
    con.commit()
    cursor.close()
    con.close()
    return id

def saveCities(cities:list):
    ids_insertados = []
    con = sqlite3.connect(ruta)
    cursor = con.cursor()
    for city in cities:
        cursor.execute("INSERT INTO ciudad (nombre, temperatura) VALUES(?,?)",city)
        ids_insertados.append(cursor.lastrowid)
    con.commit()
    cursor.close()
    con.close()

    return ids_insertados
