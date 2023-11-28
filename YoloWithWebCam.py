# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 18:50:36 2023

@author: hjr
"""
from ultralytics import YOLO
import cv2
import math 
import paho.mqtt.client as paho
from paho import mqtt
from datetime import datetime
import json


# définir des rappels pour différents événements pour voir si cela fonctionne, imprimer le message, etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# avec cette appel on peut vérifier si la publication a réussi 
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# afficher le topic qu'on va utilisé
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# mprimer un message, utile pour vérifier si l'opération a réussi
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# en utilisant MQTT version 5 ici, pour 3.1.1 : MQTTv311, 3.1 : MQTTv31
# userdata est une donnée définie par l'utilisateur de tout type, mise à jour par user_data_set()
# client_id est le prénom du client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# activer TLS pour une connexion sécurisée
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# définir le nom d'utilisateur et le mot de passe
client.username_pw_set("souhail", "Hs@16071998")
# connectez a HiveMQ Cloud sur le port 8883 (par défaut pour MQTT)
client.connect("61008efe1d534822a830a4f7aa032b30.s1.eu.hivemq.cloud", 8883)

# définition des rappels, utilisez des fonctions distinctes comme ci-dessus pour une meilleure visibilité
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


# démarrer la webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# les classes d'objet
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]


while True:
         
    success, img = cap.read()
    results = model(img, stream=True)

    # coordonnées
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # boîte englobante
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # mettre la boîte dans la caméra
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confiance
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # non du classe détécté
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])
            # objet datetime contenant la date et l'heure actuelles
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            print("date and time =", dt_string)
           
            # détails de l'objet
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            # la définition du coleur , text a afficher etc. de la boite de détectation
            cv2.putText(img, classNames[cls]+" "+str(confidence), org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    # En cliqunt sur Q
    if cv2.waitKey(1) == ord('q'):
        # x objet python
        x = { "class": classNames[cls] , "confidence" : confidence , "datetime" : dt_string}
        # convert l'objet x vers JSON
        y = json.dumps(x)
        # subscribe du topic iot
        client.subscribe("iot/#", qos=1)
        # publish de l'objet JSON y vers le topic iot
        client.publish("iot", payload=y, qos=1)
   
    
client.loop_forever()
cap.release()
cv2.destroyAllWindows()
