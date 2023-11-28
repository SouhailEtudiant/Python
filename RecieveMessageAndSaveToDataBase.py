
import mysql.connector
import paho.mqtt.client as paho
from paho import mqtt
import json


# Connection au base de données MYSQL Local
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hajri@1998",
  database ="iot"
)
# définir des rappels pour différents événements pour voir si cela fonctionne, imprimer le message, etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

 

# imprimer le  topic subscribed
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Lire un message envoyer au topic (Hive MQ) , le parser puisque il est de type JSON , puis il insert au base 
# de donneés les information Lu 
def on_message(client, userdata, msg):
    print(str(msg.payload))
    y = json.loads(msg.payload)
    mycursor = mydb.cursor()
    sql = "INSERT INTO objet (ClassName, confidence,date) VALUES (%s, %s, %s)"
    val = (y["class"], y["confidence"],y["datetime"])
    mycursor.execute(sql, val)
    mydb.commit()


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


# activer TLS pour une connexion sécurisée
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# définir le nom d'utilisateur et le mot de passe
client.username_pw_set("souhail", "Hs@16071998")
# connectez-vous à HiveMQ Cloud sur le port 8883 (par défaut pour MQTT)
client.connect("61008efe1d534822a830a4f7aa032b30.s1.eu.hivemq.cloud", 8883)

# définition des rappels, utilisez des fonctions distinctes comme ci-dessus pour une meilleure visibilité
client.on_subscribe = on_subscribe
client.on_message = on_message
 
client.subscribe("iot/#", qos=1)

client.loop_forever()