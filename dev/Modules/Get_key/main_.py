from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from ReadPorts import read_ports  # Импорт вашей функции ReadPort из src/read_ports.py
import os

# Инициализация приложения Flask
app = Flask(__name__)

# Включение CORS
CORS(app)

# Инициализация Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")


# Обрабатываем подключение клиентов по вебсокету
@socketio.on('connect')
def handle_connect():
    print(f"Клиент подключен: {request.sid}")
    read_ports(socketio)


# Обрабатываем отключение клиентов по вебсокету
@socketio.on('disconnect')
def handle_disconnect():
    print(f"Клиент отключен: {request.sid}")

# Запускаем сервер Flask
if __name__ == '__main__':
    # Запуск HTTP-сервера
    port = int(os.getenv("PORT", 3001))
    app.run(host='0.0.0.0', port=port, debug=True)

    # Запуск Socket.IO-сервера
    socketio.run(app, host='0.0.0.0', port=8999)
