from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
        )
    ''')
    conn.commit()
    conn.close()


# Сохранение сообщения в базу данных
@app.route('/api/receive', methods=['POST'])
def save_message():
    print("2")
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Encrypted message is required'}), 400

    # Здесь должна быть логика расшифровки
    # Например:
    # message = decrypt_message(encrypted_message)
    # user_id = <вытянуть из расшифрованных данных>

    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, message))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'timestamp': timestamp}), 201

# Получение новых сообщений
@app.route('/api/get/messages', methods=['POST'])
def get_messages():
    data = request.json

    last_timestamp = data.get("last_timestamp", "None")

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    if last_timestamp == "None":
        cursor.execute('SELECT user_id, message, timestamp FROM messages ORDER BY timestamp ASC')
    else:
        cursor.execute(
            'SELECT user_id, message, timestamp FROM messages WHERE timestamp > ? ORDER BY timestamp ASC',
            (last_timestamp,)  # Исправлено: передаем как кортеж
        )

    messages = cursor.fetchall()
    conn.close()

    result = [{'user_id': msg[0], 'message': msg[1], 'timestamp': msg[2]} for msg in messages]
    return jsonify({'messages': result})


@app.route('/', methods=['GET'])
def index():
    return {"its": "work"}

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5500)
