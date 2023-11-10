#
# Copyright 2021 HiveMQ GmbH
# TestDocker PUSH
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import mysql.connector
import time
import paho.mqtt.client as paho
from paho import mqtt
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hajri@1998",
  database ="iot"
)
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

 

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(str(msg.payload))
    y = json.loads(msg.payload)
    mycursor = mydb.cursor()
    sql = "INSERT INTO objet (ClassName, confidence,date) VALUES (%s, %s, %s)"
    val = (y["class"], y["confidence"],y["datetime"])
    mycursor.execute(sql, val)
    mydb.commit()

# the result is a Python dictionary:
# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("souhail", "Hs@16071998")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("61008efe1d534822a830a4f7aa032b30.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
 
# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("iot/#", qos=1)

# a single publish, this can also be done in loops, etc.
 
# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()