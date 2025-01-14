from libc.stdlib cimport rand
from libc.string cimport memcpy
from libc.string cimport memset
from libc.stdlib cimport malloc, free
import os

# Определения констант
cdef int BLOCK_SIZE = 16  # Блок в байтах
cdef int KEY_SIZE = 32    # Размер ключа в байтах

# Примерные таблицы для S-преобразования
cdef unsigned char S_BOX[256]
memset(S_BOX, 0, sizeof(S_BOX))

# Теперь заполните значения
S_BOX[:] = [
    0xFC, 0xEE, 0xDD, 0x11, 0xCF, 0x6E, 0x31, 0x16,
    0xFB, 0xC4, 0xFA, 0xDA, 0x23, 0xC5, 0x04, 0x4D,
    0xE9, 0x77, 0xF0, 0xDB, 0x93, 0x2E, 0x99, 0xBA,
    0x17, 0x36, 0xF1, 0xBB, 0x14, 0xCD, 0x5F, 0xC1,
    0xF9, 0x18, 0x65, 0x5A, 0xE2, 0x5C, 0xEF, 0x21,
    0x81, 0x1C, 0x3C, 0x89, 0xFF, 0xC8, 0xAA, 0xD4,
    0xE4, 0xA0, 0x8C, 0x0A, 0xD7, 0x74, 0xA2, 0x73,
    0x3E, 0x6B, 0x47, 0x0D, 0x61, 0x35, 0x2F, 0x4B,
    0x3A, 0x46, 0x3D, 0xD6, 0x71, 0x6F, 0x9A, 0x9E,
    0xB9, 0x72, 0x79, 0x78, 0x09, 0x3B, 0x0F, 0x1E,
    0x00, 0x86, 0xB3, 0x68, 0x57, 0xD5, 0x8B, 0x5D,
    0xD9, 0x3F, 0x53, 0x02, 0xF6, 0x6A, 0xB5, 0x1D,
    0x3F, 0x3B, 0x26, 0xA3, 0x15, 0xB6, 0xC6, 0xAC,
    0xA7, 0x1B, 0x2C, 0x27, 0x4A, 0x56, 0x4F, 0x16,
    0x9F, 0x0C, 0x9B, 0x1A, 0x5B, 0xB2, 0x5C, 0xD0,
    0xA9, 0x48, 0xB8, 0xF9, 0x6C, 0x6D, 0xC2, 0x49,
    0xB1, 0x8E, 0xA8, 0x7D, 0xF3, 0xC7, 0x7B, 0x0B,
    0xA5, 0xF2, 0x13, 0xF7, 0x31, 0x52, 0xEA, 0x33,
    0x9C, 0xDE, 0x7A, 0x22, 0xAD, 0x58, 0x32, 0x1F,
    0x77, 0x87, 0xA6, 0x30, 0x03, 0x8F, 0x20, 0x2A,
    0x11, 0x7C, 0x04, 0x50, 0x82, 0xBF, 0x85, 0x91,
    0x3A, 0xD3, 0x42, 0xC9, 0x43, 0xC4, 0xFE, 0x8A,
    0x1C, 0x12, 0x7F, 0x2E, 0x93, 0x90, 0xFF, 0x38,
    0x08, 0xE5, 0x60, 0x66, 0xE7, 0xDD, 0x41, 0xF5,
    0x45, 0x2F, 0x47, 0x40, 0x8B, 0xDB, 0xB7, 0x6B,
    0x28, 0x8D, 0x64, 0x39, 0x6F, 0x80, 0x37, 0x34,
    0x5F, 0xE8, 0xEC, 0xAE, 0xB0, 0x7C, 0x6E, 0x9D,
    0xA2, 0xE1, 0x9E, 0x84, 0xBE, 0xD2, 0x4C, 0xB4,
    0xF4, 0x2D, 0x96, 0x75, 0xC5, 0x67, 0x29, 0x53,
    0x88, 0xA4, 0x24, 0xB1, 0x98, 0x83, 0xA1, 0x1D,
    0xBD, 0xD9, 0xCC, 0xC3, 0x18, 0x94, 0x99, 0xB5,
    0x0E, 0x0F, 0x0A, 0xB9, 0x9B, 0x9A, 0x76, 0x19,
]

# Функция S-преобразования
cdef bytes s_transform(bytes block):
    cdef unsigned char *result = <unsigned char *> malloc(BLOCK_SIZE)  # Динамическое выделение памяти
    if not result:
        raise MemoryError("Failed to allocate memory for result")

    for i in range(BLOCK_SIZE):
        result[i] = S_BOX[block[i]]

    # Преобразуем результат в Python bytes и освобождаем память
    output = bytes([result[i] for i in range(BLOCK_SIZE)])
    free(result)
    return output

# Функция L-преобразования
cdef bytes l_transform(bytes block):
    cdef unsigned char *result = <unsigned char *> malloc(BLOCK_SIZE)  # Динамическое выделение памяти
    if not result:
        raise MemoryError("Failed to allocate memory for result")

    cdef const unsigned char *block_ptr = <const unsigned char *> block

    # Копируем данные из block в result
    memcpy(result, block_ptr, BLOCK_SIZE)

    cdef int i, j
    for i in range(BLOCK_SIZE):
        for j in range(8):
            result[i] ^= result[(i + j) % BLOCK_SIZE]

    # Преобразуем результат в Python bytes и освобождаем память
    output = bytes([result[i] for i in range(BLOCK_SIZE)])
    free(result)
    return output

# Основная функция шифрования
def encrypt(bytes plaintext):
    cdef bytes transformed = s_transform(plaintext)
    transformed = l_transform(transformed)
    return transformed
