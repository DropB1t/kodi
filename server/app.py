from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from camera import VideoCamera
import eventlet

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
topic_pub = 'prsn/0000/camera'
topic_sub = 'prsn/0000/cameraReply'

mqtt_client = Mqtt(app)

"""  App Routes """

@app.route("/")
@app.route("/index")
def index():
   return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        mqtt_client.publish(topic_pub, frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return app.response_class(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic_sub)
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, msg):
   if msg.topic == topic_sub:
      print('Received message on topic: {topic} with payload: {payload}'.format(msg.topic,msg.payload))

@mqtt_client.on_publish()
def on_publish(client,userdata,result):
   print("Data published \n")

""" @app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return app.make_response({'code': publish_result[0]})
 """

if __name__ == "__main__":
   app.debug = True;
   app.run(debug=True, use_reloader=False)
