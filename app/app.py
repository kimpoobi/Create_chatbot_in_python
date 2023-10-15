from flask import Flask, render_template
from flask_socketio import SocketIO, send
import pickle
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer
from sklearn.pipeline import Pipeline
import string


app = Flask(__name__)
app.config['SECRET'] = 'somethingelse'
socketio = SocketIO(app, cors_allowed_origins="*")

def cleaner(x):
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]
def bot_replay(message):
    pred_msg = ""
    with open('static/models/dclf.pkl', 'rb') as f:
        clf2 = pickle.load(f)
        pred_msg = clf2.predict([message])[0]
    
    return pred_msg

@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if message != "User Connected!":
        send(message, broadcast=True)
        send("[Bot]: " + bot_replay(message), broadcast=True)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True, host="localhost")