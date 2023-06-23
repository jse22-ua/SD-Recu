#import argparse
import socket
import sys
import urllib
from kafka import KafkaConsumer
from kafka import KafkaProducer

#parser = argparse.ArgumentParser()
#parser.add_argument("ip_engine", type = str)
#parser.add_argument("puerto_engine", type = int)
#parser.add_argument("ip_gestor", type = str)
#parser.add_argument("puerto_gestor", type = int)
#parser.add_argument("ip_registry", type = str)
#parser.add_argument("puerto_registry", type = int)
#args = parser.parse_args()/*

if(len(sys.argv) != 7):
    print(f"Argumentos incorrectos: IPENGINE PORTENGINE IPGESTOR PORTGESTOR IPREG PORTREG")
    exit()
    
#DECLARACIONES
bs = "" + sys.argv[3] + ":" + sys.argv[4]

HEADER = 64
ADDR_REGISTRY = (sys.argv[5], int(sys.argv[6]))
ADDR_ENGINE = (sys.argv[1], int(sys.argv[2]))
ADDR_GESTOR = (sys.argv[3], int(sys.argv[4]))
FORMAT = 'utf-8'
FIN = "FIN"

myPlayer_id = 0
 
def crear_perfil():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR_REGISTRY)
    print (f"Establecida conexión en [{ADDR_REGISTRY}]")

    msg = "Conectado"
    while msg != FIN :
        print("Envio al servidor: ", msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        recibido = client.recv(2048).decode(FORMAT)
        print("Recibo del Servidor: ", recibido)
        if(recibido == FIN):
            msg = FIN
        else:
            msg=input()

    print ("CONEXION FINALIZADA")
    if recibido != FIN:
        print("Envio al servidor: ", FIN)
        message = FIN.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)


def unirse_partida():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR_ENGINE)
    print (f"Establecida conexión en [{ADDR_ENGINE}]")

    msg = "Conectado"
    while msg != FIN :
        print("Envio al servidor: ", msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        recibido = client.recv(2048).decode(FORMAT)
        print("Recibo del Servidor: ", recibido)
        if(recibido == FIN):
            idrecibida = int(client.recv(2048).decode(FORMAT))
            myPlayer_id = idrecibida
            msg = FIN
        else:
            msg=input()

    print ("CONEXION FINALIZADA")
    if recibido != FIN:
        print("Envio al servidor: ", FIN)
        message = FIN.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
    jugar()
    
def showMenu():
    print ("(q   w     e)")
    print ("(a jugador d)")
    print ("(z   x     c)")
    print("pulse una de las letras alrededor del jugador")

#JUGADOR NORMAL
opcion = 0

while opcion != 3:
    print(f"1 CREAR/EDITAR perfil\n2 UNIRSE A PARTIDA\n3 Salir")
    opcion = int(input())
    if opcion == 1:
        crear_perfil()
    elif opcion == 2:
        unirse_partida()
    elif opcion == 3:
        pass
    else:
        print(f"Opcion incorrecta")


def jugar():

    partida_fin=False
    respuesta = ""
    directions = [ 'q','w','e','a','d','z','s','x']
    while not partida_fin:
    
        while True:
            showMenu()
            respuesta = input("¿Que direccion quiere tomar? ") 
            if respuesta in directions:
                break

        producer = KafkaProducer(bootstrap_servers=bs)    
        producer.send('moviments',key=myPlayer_id(4,'big') ,value=respuesta.encode('utf-8'))
        consumer = KafkaConsumer('mapa',bootstrap_servers=bs)
        for message in consumer:
            if int.from_bytes(message.key,byteorder='big') == myPlayer_id:
                if message.value.decode('utf-8') == "you died":
                    partida_fin = True
                print(message.value.decode('utf-8'))
                break
                