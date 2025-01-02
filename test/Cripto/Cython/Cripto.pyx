import numpy as np

cdef int BLOCK_SIZE = 16  # Размер блока данных
cdef int KEY_SIZE = 32    # Размер ключа данных

# Таблицы замен S-box и обратная S-box
cdef unsigned char S_BOX[256] = [
    # Таблица замены здесь...
]

cdef unsigned char INV_S_BOX[256] = [
    # Обратная таблица замены здесь...
]

# --- Линейное преобразование ---
def apply_linear_transformation(input_block: BlockType) -> BlockType:
    """
    Применяет линейное преобразование к входному блоку данных.
    """
    cdef unsigned char i
    cdef unsigned char t
    cdef BlockType output_block = np.zeros(BLOCK_SIZE, dtype=np.uint8)

    for i in range(BLOCK_SIZE):
        t = 0
        for j in range(8):  # Сложение по модулю 2
            t ^= multiply_in_field(input_block[i], L_MATRIX[i][j])
        output_block[i] = t

    return output_block

# --- Обратное линейное преобразование ---
def apply_inverse_linear_transformation(input_block: BlockType) -> BlockType:
    """
    Применяет обратное линейное преобразование к входному блоку данных.
    """
    # Реализация по аналогии с линейным преобразованием
    cdef unsigned char i, j, t
    cdef BlockType output_block = np.zeros(BLOCK_SIZE, dtype=np.uint8)

    for i in range(BLOCK_SIZE):
        t = 0
        for j in range(8):  # Инверсная логика
            t ^= multiply_in_field(input_block[i], INV_L_MATRIX[i][j])
        output_block[i] = t

    return output_block

# --- Функция умножения в поле Галуа ---
cdef unsigned char multiply_in_field(unsigned char a, unsigned char b):
    """
    Умножает два элемента в поле Галуа GF(2^8) по модулю порождающего многочлена.
    """
    cdef unsigned char result = 0
    cdef int i

    for i in range(8):
        if b & 1:  # Если младший бит b равен 1
            result ^= a  # Сложение по модулю 2
        # Сдвиг b вправо
        b >>= 1
        # Проверка старшего бита a
        carry = a & 0x80
        a <<= 1  # Сдвиг a влево
        if carry:  # Если был перенос
            a ^= 0x1C3  # XOR с порождающим многочленом

    return result & 0xFF

# --- Замена байтов с использованием S-box ---
def substitute_bytes(input_block: BlockType) -> BlockType:
    """
    Применяет S-box к каждому байту блока.
    """
    cdef int i
    cdef BlockType output_block = np.zeros(BLOCK_SIZE, dtype=np.uint8)

    for i in range(BLOCK_SIZE):
        output_block[i] = S_BOX[input_block[i]]

    return output_block

# --- Обратная замена байтов ---
def inverse_substitute_bytes(input_block: BlockType) -> BlockType:
    """
    Применяет обратный S-box к каждому байту блока.
    """
    cdef int i
    cdef BlockType output_block = np.zeros(BLOCK_SIZE, dtype=np.uint8)

    for i in range(BLOCK_SIZE):
        output_block[i] = INV_S_BOX[input_block[i]]

    return output_block

# --- XOR двух блоков ---
def xor_blocks(block1: BlockType, block2: BlockType) -> BlockType:
    """
    Выполняет побитовый XOR для двух блоков данных.
    """
    cdef int i
    cdef BlockType output_block = np.zeros(BLOCK_SIZE, dtype=np.uint8)

    for i in range(BLOCK_SIZE):
        output_block[i] = block1[i] ^ block2[i]

    return output_block

# --- Функция линейного преобразования ---
def linear_transformation(input_block: BlockType) -> BlockType:
    """
    Выполняет линейное преобразование блока.
    """
    cdef int i, j
    cdef BlockType temp_block = np.zeros(BLOCK_SIZE, dtype=np.uint8)
    cdef unsigned char temp

    for i in range(BLOCK_SIZE):
        temp = 0
        for j in range(BLOCK_SIZE):
            temp ^= multiply_in_field(input_block[j], L_MATRIX[i][j])
        temp_block[i] = temp

    return temp_block

# --- Обратное линейное преобразование ---
def inverse_linear_transformation(input_block: BlockType) -> BlockType:
    """
    Выполняет обратное линейное преобразование блока.
    """
    cdef int i, j
    cdef BlockType temp_block = np.zeros(BLOCK_SIZE, dtype=np.uint8)
    cdef unsigned char temp

    for i in range(BLOCK_SIZE):
        temp = 0
        for j in range(BLOCK_SIZE):
            temp ^= multiply_in_field(input_block[j], INV_L_MATRIX[i][j])
        temp_block[i] = temp

    return temp_block

# --- Применение функции раунда ---
def round_function(input_block: BlockType, round_key: BlockType) -> BlockType:
    """
    Выполняет один раунд шифрования: SubBytes -> LinearTransformation -> XOR с ключом.
    """
    cdef BlockType temp_block = substitute_bytes(input_block)
    temp_block = linear_transformation(temp_block)
    temp_block = xor_blocks(temp_block, round_key)

    return temp_block

# --- Основная функция шифрования одного блока ---
def encrypt_block(input_block: BlockType, round_keys: np.ndarray) -> BlockType:
    """
    Шифрует один блок данных с использованием 10 раундов.
    """
    cdef int i
    cdef BlockType temp_block = xor_blocks(input_block, round_keys[0])

    for i in range(1, 10):  # Выполнение 9 раундов
        temp_block = round_function(temp_block, round_keys[i])

    # Последний раунд без линейного преобразования
    temp_block = substitute_bytes(temp_block)
    temp_block = xor_blocks(temp_block, round_keys[10])

    return temp_block

# --- Основная функция расшифрования одного блока ---
def decrypt_block(input_block: BlockType, round_keys: np.ndarray) -> BlockType:
    """
    Расшифровывает один блок данных с использованием 10 раундов.
    """
    cdef int i
    cdef BlockType temp_block = xor_blocks(input_block, round_keys[10])

    # Первый этап: обратная замена байтов
    temp_block = inverse_substitute_bytes(temp_block)

    for i in range(9, 0, -1):  # 9 раундов в обратном порядке
        temp_block = xor_blocks(temp_block, round_keys[i])
        temp_block = inverse_linear_transformation(temp_block)
        temp_block = inverse_substitute_bytes(temp_block)

    # Финальный этап: XOR с первым ключом
    temp_block = xor_blocks(temp_block, round_keys[0])

    return temp_block

# --- Функция шифрования в режиме CTR ---
def ctr_mode_encrypt(plaintext: np.ndarray, key: BlockType, iv: BlockType) -> np.ndarray:
    """
    Шифрует данные в режиме счётчика (CTR).
    """
    cdef int i
    cdef BlockType counter, encrypted_counter, block
    cdef np.ndarray ciphertext = np.zeros_like(plaintext)
    cdef np.ndarray round_keys = generate_round_keys(key)

    counter = iv.copy()

    for i in range(0, len(plaintext), BLOCK_SIZE):
        encrypted_counter = encrypt_block(counter, round_keys)
        block = plaintext[i:i + BLOCK_SIZE]
        ciphertext[i:i + BLOCK_SIZE] = xor_blocks(block, encrypted_counter)

        # Увеличение счётчика
        counter = increment_counter(counter)

    return ciphertext

# --- Увеличение счётчика ---
def increment_counter(counter: BlockType) -> BlockType:
    """
    Инкрементирует значение счётчика.
    """
    cdef int i
    cdef BlockType new_counter = counter.copy()

    for i in range(BLOCK_SIZE - 1, -1, -1):
        if new_counter[i] < 0xFF:
            new_counter[i] += 1
            break
        else:
            new_counter[i] = 0

    return new_counter

def example_usage():
    """
    Пример использования алгоритма 'Кузнечик' для шифрования и расшифрования.
    """
    plaintext = np.array([0x32, 0x43, 0xF6, 0xA8, 0x88, 0x5A, 0x30, 0x8D,
                          0x31, 0x31, 0x98, 0xA2, 0xE0, 0x37, 0x07, 0x34], dtype=np.uint8)
    master_key = np.array([0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6,
                           0xAB, 0xF7, 0xCF, 0x83, 0x93, 0x48, 0xD8, 0x17], dtype=np.uint8)
    iv = np.array([0x00] * BLOCK_SIZE, dtype=np.uint8)

    print("Plaintext:", plaintext)
    print("Key:", master_key)

    ciphertext = ctr_mode_encrypt(plaintext, master_key, iv)
    print("Ciphertext:", ciphertext)
