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
@app.route('/api/get/messages', methods=['GET'])
def get_messages():
    data = request.json
    user_id = data['user_id']
    last_timestamp = request.args.get('last_timestamp')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    if last_timestamp:
        cursor.execute(
            'SELECT id, message, timestamp FROM messages WHERE user_id = ? AND timestamp > ? ORDER BY timestamp ASC',
            (user_id, last_timestamp))
    else:
        cursor.execute('SELECT id, message, timestamp FROM messages WHERE user_id = ? ORDER BY timestamp ASC',
                       (user_id,))

    messages = cursor.fetchall()
    conn.close()

    # Здесь должна быть логика шифрования перед отправкой
    # Например:
    # encrypted_messages = encrypt_messages(messages)

    return jsonify({'messages': messages})

@app.route('/', methods=['GET'])
def index():
    return {"its": "work"}

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5500)
