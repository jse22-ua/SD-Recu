import sys
import requests
import sqlite3
import socket
import threading
import random
from Board import Board
from NPC import NPC
from Player import Player
from Exceptions.TooManyPlayersException import TooManyPlayersException
from DB import *

FORMAT = 'utf-8'
HEADER = 64
FIN = "FIN"

arguments = sys.argv

if len(arguments) != 3:
    print("Número de argumentos incorrectos")
    print("./AA_Engine puerto_escucha numero_max_jugadores")
    exit()

PORT = sys.argv[1]
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, int(PORT))

url = "http://api.openweathermap.org/data/2.5/weather"
clave_api = open("api_clave", "r").read()


def get_city(city):
    params = {
        "appid": clave_api,
        "q": city
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['main']['temp']
    return None

def toGrades(kelvin):
    return kelvin - 273

all_cities = open("ciudades.txt","r").readlines()

cities = []
new_city = random.sample(all_cities,k=4)

for i in range(4):
    temperature = get_city(new_city[i])
    city = new_city[i].replace("\n", "")
    if temperature is None:
        print("fallo la conexión el servidor de clima")
        print(f"Procediendo a usar valores por defecto de {new_city[i]}")
        temperature = random.randint(270,300)
    cities.append((city,int(toGrades(temperature))))

print(cities)
ids = saveCities(cities)

board = Board(20,20,arguments[2],cities)
mapa_id = saveBoard(board,ids)

iniciada = False
print(board.showBoard())

MAX_CONEXIONES = board.max_players

def handle_client(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    if msg == "Conectado":
        print(f"[NUEVO JUGADOR] {addr} connected.")
        encontrado = False
    while encontrado == False:
        #PEDIMOS LOS DATOS
        conn.send(f"Escriba el nombre de su personaje".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            usuario = conn.recv(msg_length).decode(FORMAT)
        conn.send(f"Escriba su contrasena".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            contrasena = conn.recv(msg_length).decode(FORMAT)
        #BUSCAMOS EN BD
        conndb = sqlite3.connect("../database.db")
        cursor = conndb.execute("select * from personaje where alias=? and user_password=?", (usuario,contrasena))
        fila = cursor.fetchone()
        #SI EXISTE
        if fila!=None:
            print(fila)
            encontrado=True
            board.addPlayer(Player(int(fila[0]),str(fila[2]), int(fila[3]), int(fila[4]), int(fila[1])))
    
    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.send(FIN.encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = 0
    print(CONEX_ACTIVAS)
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS += 1
        if (int(CONEX_ACTIVAS) <= int(MAX_CONEXIONES)): 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[JUGADORES ACTIVOS] {CONEX_ACTIVAS}")
            print("JUGADORES RESTANTES PARA LLENAR EL SERVICIO", int(MAX_CONEXIONES)-int(CONEX_ACTIVAS))
        else:
            print("OOppsss... DEMASIADOS JUGADORES. ESPERANDO A QUE ALGUIEN SE VAYA")
            conn.send("OOppsss... DEMASIADOS JUGADORES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            #en este caso guardo en conex_actuales el  numero de personas que ya se conectaron
#            CONEX_ACTUALES = threading.active_count()-1


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("Servidor registry inicializándose...")

start()
