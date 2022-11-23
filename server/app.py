from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import eventlet
import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
@app.route("/index")
def index():
   now = datetime.datetime.now()
   timeString = now.strftime("%H:%M %m-%d")
   templateData = {
      'time': timeString
   }
   return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(debug=True)

