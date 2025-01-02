from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, template_folder='templates')

# Список для хранения сообщений
messages = []

# Адрес для пересылки сообщений
FORWARD_URL = "https://example.com/endpoint"  # Замените на нужный URL


@app.route('/api/send', methods=['POST'])
def send_message():
    """Получение сообщения от клиента и пересылка на указанный адрес."""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    message = data['message']
    messages.append({'type': 'sent', 'message': message})
    print(f"Отправлено: {message}")
    print("m:", messages)

    # Пересылаем сообщение на указанный веб-адрес
    try:
        response = requests.post(FORWARD_URL, json={'message': message})
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to forward message: {str(e)}'}), 500

    return jsonify({'success': True})


@app.route('/api/receive', methods=['POST'])
def receive_message():
    """Получение сообщения от внешнего источника."""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    message = data['message']
    messages.append({'type': 'received', 'message': message})
    print(f"Получено: {message}")

    return jsonify({'success': True})


@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Возвращает список сообщений."""
    return jsonify(messages)


@app.route('/')
def serve_chat_page():
    """Возвращает HTML-страницу чата."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
