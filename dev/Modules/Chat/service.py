import json
import os
from dev.config import requests, jsonify, FORWARD_URL, cripto, restore_key, messages_list


def encrypt_message(message):
    cripto_text = cripto.go_to_encrtipto_message(message)
    return ''.join([''.join(format(byte, '02x') for byte in array) for array in cripto_text])


def decrypt_message(message):
    blocks = cripto.block(message['messages'])

    hex_to_bin = [cripto.hex_to_bin(block) for block in blocks]
    decrypt = cripto.go_to_decrtipto_message(hex_to_bin)
    return decrypt


def generate_key(Key: str):
    print("ea")
    restore_key.original_bits = Key
    restoring_bite_code = restore_key.generate_bite()
    cripto.KEY = Key
    cripto.key_dev()

    # Пересылаем сообщение на указанный веб-адрес
    try:
        response = requests.post(FORWARD_URL + '/api/editKey', json={
            'type': 'received',
            'message': restoring_bite_code
        })
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to forward message!!!!!!: {str(e)}'}), 500


def send_message(data):
    print("1111")
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    message = data['message']

    # Пересылаем сообщение на указанный веб-адрес
    try:
        response = requests.post('https://vkr.npi24.keenetic.link/api/receive', json={
            "user_id": os.environ.get("user_id"),
            'message': message
        })

    except requests.RequestException as e:
        print("21")
        return jsonify({'error': f'Failed to forward message: {str(e)}'}), 500

    return response.json()


def receive_message():
    try:
        cripto_text = requests.post('https://vkr.npi24.keenetic.link/api/get/messages', json={
                "user_id": os.environ.get("user_id")})
        print("cripto_text", cripto_text.json())
        messages = cripto_text # json.loads(decrypt_message(cripto_text).replace("'", '"'))

        for msg in messages:
            msg["type"] = "received" if msg["type"] == "sent" else "sent"
        return messages
    except Exception as e:
        return jsonify({'error': f'Failed to forward message: {str(e)}'}), 500


