from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
from camera import Camera
import eventlet

eventlet.monkey_patch()

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883

mqtt = Mqtt(app)
socketio = SocketIO(app)

camera = Camera()
imgCount = 0

# TODO Creare un Config Parser

#mqtt.broker_url = 'broker.emqx.io'
#mqtt.broker_port = 1883

recognition_pub = 'prsn/0000/camera'
recognition_reply = 'prsn/0000/cameraReply'

emotion_pub = 'emt/0000/camera'
emotion_reply = 'emt/0000/cameraReply'

music_ranking_pub = 'adv/0000/musicRanking'
place_ranking_pub = 'adv/0000/placeRanking'

music_list_reply = 'adv/0000/musicList'
place_list_reply = 'adv/0000/placeList'

"""
lista generica di consigli
{
    [{},{},...]
}
{
    id: int,
    adv: string,
}
"""

""" App Routes """

@app.route("/")
def index():
    return render_template('index.html')

""" TODO
Dopo 21 iterazioni finisci di publicare verso il topic (codificato con base64), quando
ricevo la risposta chiudo lo streming di video in front-end e faccio redirect alle alternative
{
    id: int
    persona: string
}

Persona "Sconosciuta"
{
    id: -1
    persona: null
}
"""

""" 
def gen(camera):
    i = 0
    while True:
        frame = camera.get_frame()
        if i < 21:
            mqtt.publish(recognition_pub, frame)
            i += 1
        if i == 21:
            print("Trasmitted successfully 21 images for face recognition")
            i += 1
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return app.response_class(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
"""

@socketio.on("request-frame", namespace="/camera-feed")
def camera_frame_requested(message):
    global imgCount
    frame = camera.get_frame()
    if frame is not None:
        if imgCount < 21:
            mqtt.publish(recognition_pub, frame)
            imgCount+= 1
        emit("new-frame", {
            "base64": frame.decode("ascii")
        })

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
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)
"""

"""
Preferendo una canzone mandi verso il topic <prsn/0000/musicPreference>, ID dell'utente, e 
la conferma della preferenza in un json ovvero <il nome della canzone>/<il nome del posto>

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
    try:
        camera.start()
        socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
    except KeyboardInterrupt:
        camera.stop()
    