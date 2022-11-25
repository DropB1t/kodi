from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from camera import VideoCamera
import eventlet
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883

mqtt = Mqtt(app)

# TODO Creare un Config Parser

#mqtt.broker_url = 'broker.emqx.io'
#mqtt.broker_port = 1883

recognition_pub = 'prsn/0000/camera'
recognition_reply = 'prsn/0000/cameraReply'

emotion_pub = 'emt/0000/camera'
emotion_reply = 'emt/0000/cameraReply'

music_ranking_pub = 'prsn/0000/musicRanking'
place_ranking_pub = 'prsn/0000/placeRanking'

""" App Routes """

@app.route("/")
def index():
    return render_template('index.html')

""" TODO
Dopo 50 iterazioni finisci di publicare verso il topic (codificato con base64 ), quando
ricevo la risposta chiudo lo streming di video in front-end e faccio redirect alle alternative
"""
def gen(camera):
    i = 0
    while True:
        payload, frame, blurred = camera.get_frame()
        if not blurred and i < 50:
            mqtt.publish(recognition_pub, payload)
            i += 1
        if i == 50:
            print("Trasmitted successfully 50 images for face recognition")
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return app.response_class(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

""" MQTT Handlers """

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt.subscribe(recognition_reply)
        mqtt.subscribe(emotion_reply)
    else:
        print('Bad connection. Code:', rc)

""" TODO
Alla ricezione dello UIID fetcho configurazione personale
della persona contenuta localmente sul sistema ( Un oggetto seriallizato )
"""
@mqtt.on_topic(recognition_reply)
def handle_recognition_reply(client, userdata, msg):
    print('Received message on topic {}: {}'.format(msg.topic, msg.payload.decode()))

@mqtt.on_topic(emotion_reply)
def handle_emotion_reply(client, userdata, msg):
    print('Received message on topic {}: {}'.format(msg.topic, msg.payload.decode()))

@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    print('Received message on topic: {topic} with payload: {payload}'.format(msg.topic, msg.payload))

@mqtt.on_publish()
def on_publish(client, userdata, result):
    print("Data published \n")

"""
Preferendo una canzone mandi verso il topic <prsn/0000/musicPreference> e 
la conferma della preferenza in un json
"""

""" WebSocketIO Dispatcher """

"""
@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return app.make_response({'code': publish_result[0]})
"""

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
