from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
from camera import Camera
import eventlet
import json
import pickle
import hashlib

eventlet.monkey_patch()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = "broker.emqx.io"
app.config['MQTT_BROKER_PORT'] = 1883

mqtt = Mqtt(app)
socketio = SocketIO(app)

camera = Camera()
imgCount = 0

user = None

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
@app.route("/login")
def login():
    global imgCount
    camera.set_pause()
    if imgCount == 21:
        imgCount = 0
    print(imgCount)
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    global user
    if user is None:
        loadUser("1Yuriy Rymarchuk")
        #return render_template("login.html")
    #camera.set_pause(1.5)
    print(user)
    return render_template("dashboard.html", name = user['user'])

@app.route("/reset")
def reset():
    global user, imgCount
    user = None
    imgCount = 0
    camera.set_pause()
    return render_template("login.html")

""" WebSocketIO Dispatcher """

@socketio.on("request-frame", namespace="/login-feed")
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

@socketio.on("request-emotion", namespace="/dashboard-feed")
def emotion_frame_requested(message):
    frame = camera.get_frame()
    if frame is not None:
        mqtt.publish(emotion_pub, frame)

""" MQTT Handlers """

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        mqtt.subscribe(recognition_reply)
        mqtt.subscribe(emotion_reply)
    else:
        print("Bad connection. Code:", rc)

@mqtt.on_topic(recognition_reply)
def handle_recognition_reply(client, userdata, msg):
    res = json.loads(msg.payload.decode())
    print('User data {}'.format(res))
    if res['id'] != -1:
        user_UID = str(res['id']) + res['user']
        loadUser(user_UID)
    socketio.emit('login-res', res, namespace="/login-feed")
    
def loadUser(user_UID:str):
    global user
    hash_uid = hashlib.sha256(user_UID.encode('utf-8')).hexdigest()
    with open('./data/' + hash_uid, "rb") as infile:
 	    user = pickle.load(infile)

@mqtt.on_topic(emotion_reply)
def handle_emotion_reply(client, userdata, msg):
    print('Received message on topic {}: {}'.format(msg.topic, msg.payload.decode()))
    res = json.loads(msg.payload.decode())
    socketio.emit('emotion-res', res, namespace="/dashboard-feed")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    print('Received message on topic: {topic} with payload: {payload}'.format(msg.topic, msg.payload.decode()))

@mqtt.on_publish()
def on_publish(client, userdata, result):
    print("Data published")

"""
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)
"""

"""
Preferendo una canzone mandi verso il topic <prsn/0000/musicPreference>, ID dell'utente, e 
la conferma della preferenza in un json ovvero <il nome della canzone>/<il nome del posto>
"""

if __name__ == "__main__":
    try:
        camera.start()
        socketio.run(app, host='127.0.0.1', port=5000, use_reloader=False, debug=True)
    except KeyboardInterrupt:
        camera.stop()
    