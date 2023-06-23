from Engine.npc import NPC
from Engine.personaje import Personaje
import random 
import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
import sys 

arguments = sys.argv

if len(arguments) != 3:
    print("Número de argumentos incorrectos")
    print("./AA_NPC IP_gestor_colas puerto_gestor_colas")
    exit()

bs = "" + sys.argv[1] + ":" + sys.argv[2]

nivel = random.randint(1,15)
directions = [ 'q','w','e','a','d','z','s','x']
producer = KafkaProducer(bootstrap_servers=bs)

MyNPC = NPC(0,nivel)
producer.send('NPCs',value=nivel.to_bytes(4,'big'))
consumer = KafkaConsumer('mapa',bootstrap_servers=bs)

while MyNPC.is_alive:
    moviment = random.choice(directions)
    producer.send('moviments',key=MyNPC.id.to_bytes(4,'big') ,value=moviment.encode('utf-8'))
    time.sleep(5)
    for message in consumer:
        if int.from_bytes(message.key,byteorder='big')== MyNPC.id:
            if message.value.decode('utf-8')=="continua":
                break
            else:
                print('has muerto') 
                exit()