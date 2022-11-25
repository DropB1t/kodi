import paho.mqtt.client as mqtt

broker="127.0.0.1"
port=1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("net/0000/cameraReply")
    
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print(msg.topic)
    print(msg.payload)

client= mqtt.Client("contro")    
client.on_message = on_message
client.on_connect = on_connect
client.connect(broker,port)

client.loop_forever()
