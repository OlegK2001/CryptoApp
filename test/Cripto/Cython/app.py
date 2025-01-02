from Kuznechik import generate_key, encrypt_block, decrypt_block


def main():
    # Генерация ключа
    key, K1, K2 = generate_key()
    print(f"Сгенерированный ключ: {type(K1.hex())}{K2}")  # Выводим ключ в шестнадцатеричном формате

    # Шифрование
    plaintext = "Это тестовое сообщение.".encode('utf-8')  # Кодируем текст в байты
    ciphertext = encrypt_block(plaintext, K1)  # Используем K1 для шифрования
    print(f"Зашифрованный текст: {ciphertext}")  # Выводим зашифрованный текст в шестнадцатеричном формате
    '''
    # Дешифрование
    decrypted_text = decrypt_block(ciphertext, K1)  # Используем K1 для дешифрования
    print(f"Расшифрованный текст: {decrypted_text.decode('utf-8')}")  # Декодируем текст из байтов в строку
    '''

if __name__ == "__main__":
    main()