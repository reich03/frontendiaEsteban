from flask import Flask, render_template, request, jsonify
import queue

app = Flask(__name__)
messages = queue.Queue()
all_messages_history = []  # Almacenar el historial completo de mensajes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/messages')
def send_messages():
    # Devolver una copia de todos los mensajes para mantener el historial
    return jsonify(messages=list(all_messages_history))

@app.route('/post', methods=['POST'])
def post():
    data = request.get_json()
    message_type = data.get('type', 'user')  # Asume que el tipo por defecto es 'user'
    new_message = {'message': data['message'], 'type': message_type}
    messages.put(new_message)  # Almacenar en la cola para procesamiento posterior
    all_messages_history.append(new_message)  # Agregar al historial completo
    return jsonify(success=True)

@app.route('/get_messages')
def get_messages():
    # Esta función recuperará mensajes de la cola para procesamiento, como por 'kokoro.py'
    received_messages = []
    while not messages.empty():
        received_messages.append(messages.get())
    return jsonify(messages=received_messages)

@app.route('/confirm_messages')
def confirm_messages():
    # Este endpoint podría usarse para confirmar el procesamiento de mensajes si es necesario
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
