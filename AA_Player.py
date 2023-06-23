#import argparse
import socket
import sys
import urllib

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

HEADER = 64
ADDR_REGISTRY = (sys.argv[5], int(sys.argv[6]))
ADDR_ENGINE = (sys.argv[1], int(sys.argv[2]))
ADDR_GESTOR = (sys.argv[3], int(sys.argv[4]))
FORMAT = 'utf-8'
FIN = "FIN"

 
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
