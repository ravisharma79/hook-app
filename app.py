from flask import Flask, jsonify
import random

app = Flask(__name__)

# A small database of video hooks
video_hooks = [
    "Stop scrolling! If you want to boost your retention, watch this.",
    "I tried the secret auto-editing tool everyone is talking about.",
    "Here is the exact script framework that keeps viewers engaged.",
    "You've been writing your video titles all wrong. Here's why."
]

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Welcome to the Video Hook Generator API! Go to /hook to get a script idea."
    })

@app.route('/hook')
def get_hook():
    selected_hook = random.choice(video_hooks)
    return jsonify({
        "hook": selected_hook,
        "advice": "Deliver this with high energy in the first 3 seconds!"
    })

if __name__ == '__main__':
    # host='0.0.0.0' is crucial for Docker to route traffic correctly later
    app.run(host='0.0.0.0', port=5000)