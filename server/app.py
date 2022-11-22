from flask import Flask, render_template
import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%H:%M %m-%d")
   templateData = {
      'time': timeString
   }
   return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(debug=True)

