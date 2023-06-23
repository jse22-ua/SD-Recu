#import argparse
import sys
import socket
import threading
import sqlite3
import random

#parser = argparse.ArgumentParser()
#parser.add_argument("puerto_escucha", type = int)
#args = parser.parse_args()

if(len(sys.argv) != 2):
    print(f"Argumentos incorrectos: PORTESCUCHA")
    exit()

#DECLARACIONES
HEADER = 64
PORT = sys.argv[1]
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, int(PORT))
FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 3

def handle_client(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    if msg == "Conectado":
        print(f"[NUEVA CONEXION] {addr} connected.")
        connected = True


    conn.send(f"Desea CREAR o EDITAR a un perfil de jugador".encode(FORMAT))
    while connected:
        #
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == FIN:
                connected = False
            elif msg == "CREAR":
                conn.send(f"Escriba un nuevo nombre de usuario:".encode(FORMAT))
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    usuario = conn.recv(msg_length).decode(FORMAT)
                conn.send(f"Escriba una contraseña:".encode(FORMAT))
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    contrasena = conn.recv(msg_length).decode(FORMAT)

                #INSERTAR EN BD
                conndb = sqlite3.connect("database.db")
                ef = random.randrange(-10, 10, 1)
                ec = random.randrange(-10, 10, 1)
                conndb.execute("insert into personaje(alias, user_password, EF, EC) values (?,?,?,?)", (str(usuario), str(contrasena), ef, ec))
                conndb.commit()
                conndb.close()

                conn.send(FIN.encode(FORMAT))
                connected = False

            elif msg == "EDITAR":
                conn.send(f"Escriba el nombre de usuario que quiere cambiar:".encode(FORMAT))
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    usuario = conn.recv(msg_length).decode(FORMAT)
                conn.send(f"Escriba la contraseña:".encode(FORMAT))
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    contrasena = conn.recv(msg_length).decode(FORMAT)
                #COMPROBAR USUARIO Y CONTRASEÑA
                conndb = sqlite3.connect("database.db")
                cursor = conndb.execute("select alias,user_password from personaje where alias=? and user_password=?", (usuario,contrasena))
                fila = cursor.fetchone()
                #SI EXISTE
                if fila!=None:
                    print(fila)
                    #SI ES CORRECTA COGER DATOS BD
                    conn.send(f"CORRECTO, a continuacion pediremos los nuevos datos\nEscriba el nuevo nombre de usuario:".encode(FORMAT))                
                    msg_length = conn.recv(HEADER).decode(FORMAT)
                    if msg_length:
                        msg_length = int(msg_length)
                        nusuario = conn.recv(msg_length).decode(FORMAT)
                    conn.send(f"Escriba la nueva contraseña:".encode(FORMAT))
                    msg_length = conn.recv(HEADER).decode(FORMAT)
                    if msg_length:
                        msg_length = int(msg_length)
                        ncontrasena = conn.recv(msg_length).decode(FORMAT)

                    #CAMBIAR EL JUGADOR QUE HEMOS CARGADO Y PASARLO A LA BD
                    conndb.execute("UPDATE personaje SET alias = ?, user_password= ? WHERE alias=? and user_password=?", (nusuario,ncontrasena,usuario,contrasena))
                    conndb.commit()
                    conndb.close()
                else:
                    print("No existe ese perfil de usuario o la contraseña es incorrecta")
                conn.send(FIN.encode(FORMAT))
                connected = False
            else:
                conn.send(f"Esa no es una opcion valida: CREAR o EDITAR".encode(FORMAT))
            #

            print(f" He recibido del cliente [{addr}] el mensaje: {msg}")
            #conn.send(f"HOLA CLIENTE: He recibido tu mensaje: {msg} ".encode(FORMAT))
    print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    print(CONEX_ACTIVAS)
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
            conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1


## MAIN ##

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("Servidor registry inicializándose...")

start()

