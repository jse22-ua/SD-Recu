import sys
import requests
import random
from Board import Board
from NPC import NPC
from Player import Player
from exceptions.TooManyPlayersException import TooManyPlayersException
from DB import *

arguments = sys.argv

if len(arguments) != 3:
    print("Número de argumentos incorrectos")
    print("./AA_Engine puerto_escucha numero_max_jugadores")
    exit()

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

''' peticiones // hacer asincrono
    while True:
        if board.n_players == board.max_players:
            #devolver mensaje en socket
        if iniciada:
            #devolver otro mensaje
        else:
            #recibir peticiones para añadir jugadores
'''
'''
    while board.n_players == 1:
        #jugar
    
'''



