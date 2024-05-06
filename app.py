from flask import Flask, render_template, request, jsonify
import queue

app = Flask(__name__)
messages = queue.Queue()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/messages')
def send_messages():
    all_messages = []
    while not messages.empty():
        all_messages.append(messages.get())
    return jsonify(messages=all_messages)

@app.route('/post', methods=['POST'])
def post():
    data = request.get_json()
    messages.put(data['message'])
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
