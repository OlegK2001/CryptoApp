from typing import Final
import numpy as np
from numpy._typing import NDArray
ValueType: Final = np.uint8
BlockType: Final = NDArray[np.uint8]
class Cripto:
    def __init__(self, key):
        self.KEY = key
        self.ValueType: Final = np.uint8
        self.BlockType: Final = NDArray[self.ValueType]
        self.BLOCK_SIZE: Final = 16
        self.KEY_SECTIONS: Final = 4
        self.ROUND_CONSTANTS_COUNT: Final = 32
        self.INITIAL_CONSTANT: Final = 1
        self.FIRST_BYTE_POS: Final = 0
        self.LAST_BYTE_POS: Final = self.BLOCK_SIZE - 1
        self.ROUNDS: Final = 10  # Количество раундов шифрования
        self.ACTUAL_ROUNDS: Final = self.ROUNDS - 1
        self.GALOIS_FIELD_MODULUS: Final = 0xC3  # Неприводимый многочлен x^8 + x^7 + x^6 + x + 1
        self.BITS_IN_BYTE: Final = 8
        self.HIGH_BIT_VALUE: Final = 0x80
        self.BYTE_VALUE_MASK: Final = 0xFF
        self.Pi: Final = np.array([
            0xFC, 0xEE, 0xDD, 0x11, 0xCF, 0x6E, 0x31, 0x16,
            0xFB, 0xC4, 0xFA, 0xDA, 0x23, 0xC5, 0x04, 0x4D,
            0xE9, 0x77, 0xF0, 0xDB, 0x93, 0x2E, 0x99, 0xBA,
            0x17, 0x36, 0xF1, 0xBB, 0x14, 0xCD, 0x5F, 0xC1,
            0xF9, 0x18, 0x65, 0x5A, 0xE2, 0x5C, 0xEF, 0x21,
            0x81, 0x1C, 0x3C, 0x42, 0x8B, 0x01, 0x8E, 0x4F,
            0x05, 0x84, 0x02, 0xAE, 0xE3, 0x6A, 0x8F, 0xA0,
            0x06, 0x0B, 0xED, 0x98, 0x7F, 0xD4, 0xD3, 0x1F,
            0xEB, 0x34, 0x2C, 0x51, 0xEA, 0xC8, 0x48, 0xAB,
            0xF2, 0x2A, 0x68, 0xA2, 0xFD, 0x3A, 0xCE, 0xCC,
            0xB5, 0x70, 0x0E, 0x56, 0x08, 0x0C, 0x76, 0x12,
            0xBF, 0x72, 0x13, 0x47, 0x9C, 0xB7, 0x5D, 0x87,
            0x15, 0xA1, 0x96, 0x29, 0x10, 0x7B, 0x9A, 0xC7,
            0xF3, 0x91, 0x78, 0x6F, 0x9D, 0x9E, 0xB2, 0xB1,
            0x32, 0x75, 0x19, 0x3D, 0xFF, 0x35, 0x8A, 0x7E,
            0x6D, 0x54, 0xC6, 0x80, 0xC3, 0xBD, 0x0D, 0x57,
            0xDF, 0xF5, 0x24, 0xA9, 0x3E, 0xA8, 0x43, 0xC9,
            0xD7, 0x79, 0xD6, 0xF6, 0x7C, 0x22, 0xB9, 0x03,
            0xE0, 0x0F, 0xEC, 0xDE, 0x7A, 0x94, 0xB0, 0xBC,
            0xDC, 0xE8, 0x28, 0x50, 0x4E, 0x33, 0x0A, 0x4A,
            0xA7, 0x97, 0x60, 0x73, 0x1E, 0x00, 0x62, 0x44,
            0x1A, 0xB8, 0x38, 0x82, 0x64, 0x9F, 0x26, 0x41,
            0xAD, 0x45, 0x46, 0x92, 0x27, 0x5E, 0x55, 0x2F,
            0x8C, 0xA3, 0xA5, 0x7D, 0x69, 0xD5, 0x95, 0x3B,
            0x07, 0x58, 0xB3, 0x40, 0x86, 0xAC, 0x1D, 0xF7,
            0x30, 0x37, 0x6B, 0xE4, 0x88, 0xD9, 0xE7, 0x89,
            0xE1, 0x1B, 0x83, 0x49, 0x4C, 0x3F, 0xF8, 0xFE,
            0x8D, 0x53, 0xAA, 0x90, 0xCA, 0xD8, 0x85, 0x61,
            0x20, 0x71, 0x67, 0xA4, 0x2D, 0x2B, 0x09, 0x5B,
            0xCB, 0x9B, 0x25, 0xD0, 0xBE, 0xE5, 0x6C, 0x52,
            0x59, 0xA6, 0x74, 0xD2, 0xE6, 0xF4, 0xB4, 0xC0,
            0xD1, 0x66, 0xAF, 0xC2, 0x39, 0x4B, 0x63, 0xB6
        ])
        self.reverse_Pi: Final = np.array([
            0xA5, 0x2D, 0x32, 0x8F, 0x0E, 0x30, 0x38, 0xC0,
            0x54, 0xE6, 0x9E, 0x39, 0x55, 0x7E, 0x52, 0x91,
            0x64, 0x03, 0x57, 0x5A, 0x1C, 0x60, 0x07, 0x18,
            0x21, 0x72, 0xA8, 0xD1, 0x29, 0xC6, 0xA4, 0x3F,
            0xE0, 0x27, 0x8D, 0x0C, 0x82, 0xEA, 0xAE, 0xB4,
            0x9A, 0x63, 0x49, 0xE5, 0x42, 0xE4, 0x15, 0xB7,
            0xC8, 0x06, 0x70, 0x9D, 0x41, 0x75, 0x19, 0xC9,
            0xAA, 0xFC, 0x4D, 0xBF, 0x2A, 0x73, 0x84, 0xD5,
            0xC3, 0xAF, 0x2B, 0x86, 0xA7, 0xB1, 0xB2, 0x5B,
            0x46, 0xD3, 0x9F, 0xFD, 0xD4, 0x0F, 0x9C, 0x2F,
            0x9B, 0x43, 0xEF, 0xD9, 0x79, 0xB6, 0x53, 0x7F,
            0xC1, 0xF0, 0x23, 0xE7, 0x25, 0x5E, 0xB5, 0x1E,
            0xA2, 0xDF, 0xA6, 0xFE, 0xAC, 0x22, 0xF9, 0xE2,
            0x4A, 0xBC, 0x35, 0xCA, 0xEE, 0x78, 0x05, 0x6B,
            0x51, 0xE1, 0x59, 0xA3, 0xF2, 0x71, 0x56, 0x11,
            0x6A, 0x89, 0x94, 0x65, 0x8C, 0xBB, 0x77, 0x3C,
            0x7B, 0x28, 0xAB, 0xD2, 0x31, 0xDE, 0xC4, 0x5F,
            0xCC, 0xCF, 0x76, 0x2C, 0xB8, 0xD8, 0x2E, 0x36,
            0xDB, 0x69, 0xB3, 0x14, 0x95, 0xBE, 0x62, 0xA1,
            0x3B, 0x16, 0x66, 0xE9, 0x5C, 0x6C, 0x6D, 0xAD,
            0x37, 0x61, 0x4B, 0xB9, 0xE3, 0xBA, 0xF1, 0xA0,
            0x85, 0x83, 0xDA, 0x47, 0xC5, 0xB0, 0x33, 0xFA,
            0x96, 0x6F, 0x6E, 0xC2, 0xF6, 0x50, 0xFF, 0x5D,
            0xA9, 0x8E, 0x17, 0x1B, 0x97, 0x7D, 0xEC, 0x58,
            0xF7, 0x1F, 0xFB, 0x7C, 0x09, 0x0D, 0x7A, 0x67,
            0x45, 0x87, 0xDC, 0xE8, 0x4F, 0x1D, 0x4E, 0x04,
            0xEB, 0xF8, 0xF3, 0x3E, 0x3D, 0xBD, 0x8A, 0x88,
            0xDD, 0xCD, 0x0B, 0x13, 0x98, 0x02, 0x93, 0x80,
            0x90, 0xD0, 0x24, 0x34, 0xCB, 0xED, 0xF4, 0xCE,
            0x99, 0x10, 0x44, 0x40, 0x92, 0x3A, 0x01, 0x26,
            0x12, 0x1A, 0x48, 0x68, 0xF5, 0x81, 0x8B, 0xC7,
            0xD6, 0x20, 0x0A, 0x08, 0x00, 0x4C, 0xD7, 0x74
        ])
        self.LINEAR_VECTOR: Final = np.array([
            0x01, 0x94, 0x20, 0x85, 0x10, 0xC2, 0xC0, 0x01,
            0xFB, 0x01, 0xC0, 0xC2, 0x10, 0x85, 0x20, 0x94
        ])
        self.iteration_constants = np.zeros((self.ROUND_CONSTANTS_COUNT, self.BLOCK_SIZE), dtype=self.ValueType)
        self.round_keys = np.zeros((self.ROUNDS, self.BLOCK_SIZE), dtype=self.ValueType)

    def xor_arrays(self, first_array: NDArray[np.uint8], second_array: NDArray[np.uint8]) -> NDArray[np.uint8]:
        if first_array.shape != second_array.shape:
            raise ValueError(
                f"Массивы должны иметь одинаковый размер. Получены: {first_array.shape} и {second_array.shape}.")

        return np.bitwise_xor(first_array, second_array)

    def apply_sbox(self, input_block: NDArray[np.uint8]) -> NDArray[np.uint8]:
        if not np.all((input_block >= 0) & (input_block < 256)):
            raise ValueError("Все значения входного массива должны быть в диапазоне от 0 до 255.")

        return self.Pi[input_block]

    def galois_field_multiply(self, first: int, second: int) -> int:
        if not (0 <= first < 256) or not (0 <= second < 256):
            raise ValueError("Оба аргумента должны быть в диапазоне от 0 до 255.")
        result = 0
        multiplicand = first
        multiplier = second
        for _ in range(self.BITS_IN_BYTE):
            if multiplier & 1:
                result ^= multiplicand
            high_bit = multiplicand & self.HIGH_BIT_VALUE
            multiplicand = (multiplicand << 1) & self.BYTE_VALUE_MASK
            if high_bit:
                multiplicand ^= self.GALOIS_FIELD_MODULUS
            multiplier >>= 1
        return result

    def create_galois_multiplication_table(self) -> NDArray[np.uint8]:
        table = np.zeros((256, 256), dtype=ValueType)
        for i in range(256):
            for j in range(256):
                table[i, j] = self.galois_field_multiply(i, j)
        return table

    def start(self):
        self.MULTIPLICATION_TABLE = self.create_galois_multiplication_table()

    def galois_field_multiply_fast(self, first: int, second: int) -> int:
        return self.MULTIPLICATION_TABLE[first, second]

    def apply_linear_transformation(self, input_block: NDArray[np.uint8]) -> NDArray[np.uint8]:
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError("Входной массив состояния должен содержать ровно BLOCK_SIZE байтов.")
        a_15 = 0
        output_block = np.zeros_like(input_block)
        for i in range(15, -1, -1):
            if i == 0:
                output_block[15] = input_block[i]
            else:
                output_block[i - 1] = input_block[i]
            a_15 ^= self.galois_field_multiply_fast(input_block[i], self.LINEAR_VECTOR[i])
        output_block[self.LAST_BYTE_POS] = a_15
        return output_block

    def apply_linear_function(self, input_block: NDArray[np.uint8]) -> NDArray[np.uint8]:
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной массив состояния должен содержать ровно {self.BLOCK_SIZE} байтов.")
        output_block = input_block
        for _ in range(self.BLOCK_SIZE):
            output_block = self.apply_linear_transformation(output_block)
        return output_block

    def apply_inverse_sbox(self, input_block: BlockType) -> BlockType:
        if not np.all((input_block >= 0) & (input_block < 256)):
            raise ValueError("Все значения входного массива должны быть в диапазоне от 0 до 255.")

        return self.reverse_Pi[input_block]

    def apply_inverse_R_function(self, input_block: BlockType) -> BlockType:
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной массив состояния должен содержать ровно {self.BLOCK_SIZE} байтов.")

        first_byte = input_block[self.LAST_BYTE_POS]
        output_block = np.zeros_like(input_block)
        for i in range(1, self.BLOCK_SIZE):
            output_block[i] = input_block[i - 1]
            first_byte ^= self.galois_field_multiply_fast(output_block[i], self.LINEAR_VECTOR[i])
        output_block[self.FIRST_BYTE_POS] = first_byte
        return output_block

    def apply_inverse_linear_function(self, input_block: BlockType) -> BlockType:
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной массив состояния должен содержать ровно {self.BLOCK_SIZE} байтов.")

        output_block = input_block
        for _ in range(self.BLOCK_SIZE):
            output_block = self.apply_inverse_R_function(output_block)
        return output_block

    def compute_round_constants(self) -> None:
        blocks = np.zeros_like(self.iteration_constants)
        blocks[:, 0] = np.arange(self.INITIAL_CONSTANT, self.ROUND_CONSTANTS_COUNT + 1)
        for i in range(self.ROUND_CONSTANTS_COUNT):
            self.iteration_constants[i] = self.apply_linear_function(blocks[i])

    def apply_feistel_round(
            self,
            key_part_1: NDArray[np.uint8],
            key_part_2: NDArray[np.uint8],
            iteration_constant: NDArray[np.uint8]
    ) -> tuple[NDArray[np.uint8], NDArray[np.uint8]]:
        for arg in [key_part_1, key_part_2, iteration_constant]:
            if arg.shape != (self.BLOCK_SIZE,):
                raise ValueError(f"Входной массив должен содержать ровно {self.BLOCK_SIZE} байтов, получено: {arg.shape}.")

        transformed_block = self.xor_arrays(key_part_1, iteration_constant)  # Операция XOR 1 части ключа со счетчиком
        transformed_block = self.apply_sbox(transformed_block)  # Применение S-функции
        transformed_block = self.apply_linear_function(transformed_block)  # Применение L-функции
        new_key_part_1 = self.xor_arrays(transformed_block, key_part_2)  # Операция XOR с результатом и второй частью ключа

        return new_key_part_1, key_part_1

    def expand_key(self, master_key_1: NDArray[np.uint8], master_key_2: NDArray[np.uint8]) -> None:
        for arg, name in zip([master_key_1, master_key_2], ["master_key_1", "master_key_2"]):
            if arg.shape != (self.BLOCK_SIZE,):
                raise ValueError(f"{name} должен содержать ровно {self.BLOCK_SIZE} байтов, получено: {arg.shape}.")

        self.compute_round_constants()

        # Инициализация раундовых ключей
        self.round_keys[0] = master_key_1
        self.round_keys[1] = master_key_2

        # Генерация ключей
        temp_keys_1 = [master_key_1, master_key_2]

        # print(KEY_SECTIONS)
        for section in range(self.KEY_SECTIONS):
            temp_keys_2 = self.apply_feistel_round(temp_keys_1[0], temp_keys_1[1], self.iteration_constants[0 + 8 * section])
            temp_keys_1 = self.apply_feistel_round(temp_keys_2[0], temp_keys_2[1], self.iteration_constants[1 + 8 * section])
            temp_keys_2 = self.apply_feistel_round(temp_keys_1[0], temp_keys_1[1], self.iteration_constants[2 + 8 * section])
            temp_keys_1 = self.apply_feistel_round(temp_keys_2[0], temp_keys_2[1], self.iteration_constants[3 + 8 * section])
            temp_keys_2 = self.apply_feistel_round(temp_keys_1[0], temp_keys_1[1], self.iteration_constants[4 + 8 * section])
            temp_keys_1 = self.apply_feistel_round(temp_keys_2[0], temp_keys_2[1], self.iteration_constants[5 + 8 * section])
            temp_keys_2 = self.apply_feistel_round(temp_keys_1[0], temp_keys_1[1], self.iteration_constants[6 + 8 * section])
            temp_keys_1 = self.apply_feistel_round(temp_keys_2[0], temp_keys_2[1], self.iteration_constants[7 + 8 * section])

            self.round_keys[2 * section + 2] = temp_keys_1[0]
            self.round_keys[2 * section + 3] = temp_keys_1[1]

    def encrypt(self, input_block: NDArray[np.uint8]) -> NDArray[np.uint8]:
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной блок должен содержать ровно {self.BLOCK_SIZE} байтов.")

        output_block = input_block
        for i in range(self.ACTUAL_ROUNDS):
            output_block = self.xor_arrays(self.round_keys[i], output_block)
            output_block = self.apply_sbox(output_block)
            output_block = self.apply_linear_function(output_block)

        output_block = self.xor_arrays(output_block, self.round_keys[self.ACTUAL_ROUNDS])
        return output_block

    def decrypt(self, input_block: NDArray[np.uint8]) -> NDArray[np.uint8]:
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной блок должен содержать ровно {self.BLOCK_SIZE} байтов.")

        output_block = self.xor_arrays(input_block, self.round_keys[self.ACTUAL_ROUNDS])
        for i in range(self.ACTUAL_ROUNDS - 1, -1, -1):
            output_block = self.apply_inverse_linear_function(output_block)
            output_block = self.apply_inverse_sbox(output_block)
            output_block = self.xor_arrays(self.round_keys[i], output_block)

        return output_block

    def hex_to_bin(self, hex_string: str) -> NDArray[np.uint8]:
        if hex_string is None or hex_string == "":
            return np.array([], dtype=ValueType)
        return np.array(bytearray.fromhex(hex_string), dtype=ValueType)

    def bin_to_hex(self, bin_array: NDArray[np.uint8]) -> str:
        if bin_array is None or len(bin_array) == 0:
            return ""
        return ''.join([f'{x:02x}' for x in bin_array])

    def main(self) -> None:
        TEST_KEY_1 = np.array([
            0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11, 0x00,
            0xFF, 0xEE, 0xDD, 0xCC, 0xBB, 0xAA, 0x99, 0x88,
        ], dtype=ValueType)

        TEST_KEY_2 = np.array([
            0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01,
            0x10, 0x32, 0x54, 0x76, 0x98, 0xBA, 0xDC, 0xFE,
        ], dtype=ValueType)

        TEST_PLAINTEXT: Final[str] = "8899aabbccddeeff0077665544332211"
        TEST_CIPHERTEXT: Final[str] = "cdedd4b9428d465a3024bcbe909d677f"

        # Преобразование входных данных
        init_block = self.hex_to_bin(TEST_PLAINTEXT)
        print(init_block)

        # Развертывание ключа
        self.expand_key(TEST_KEY_1, TEST_KEY_2)

        # Шифрование
        encrypted_block = self.encrypt(init_block)
        print(encrypted_block)
        # Проверка результата шифрования
        assert self.bin_to_hex(encrypted_block) == TEST_CIPHERTEXT, "Encryption failed!"

        # Расшифрование
        decrypted_block = self.decrypt(encrypted_block)
        print(decrypted_block)
        # Проверка результата расшифрования
        assert self.bin_to_hex(decrypted_block) == TEST_PLAINTEXT, "Decryption failed!"
        print("Encryption and decryption successful!")


Code = Cripto("key")
Code.start()
Code.main()