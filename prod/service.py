import json

from config import requests, jsonify, FORWARD_URL, cripto


def encrypt_message(message):
    cripto_text = cripto.go_to_encrtipto_message(message)
    return ''.join([''.join(format(byte, '02x') for byte in array) for array in cripto_text])


def decrypt_message(message):
    blocks = cripto.block(message['messages'])
    hex_to_bin = [cripto.hex_to_bin(block) for block in blocks]
    decrypt = cripto.go_to_decrtipto_message(hex_to_bin)
    return decrypt.replace("\x00", '')


def generate_key(Key: str):
    cripto.KEY = Key
    cripto.key_dev()


def send_message(data):
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    message = data['message']
    # Пересылаем сообщение на указанный веб-адрес
    try:
        response = requests.post(FORWARD_URL + '/api/receive', json={
            'type': 'received',
            'message': encrypt_message(message)
        })
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to forward message!!!!!!: {str(e)}'}), 500

    return response.json()


def receive_message():
    cripto_text = requests.get(FORWARD_URL + '/api/get/messages').json()
    messages = json.loads(decrypt_message(cripto_text).replace("'", '"'))
    for msg in messages:
        msg["type"] = "received" if msg["type"] == "sent" else "sent"
    return messages
