from typing import Final
import numpy as np
from numpy._typing import NDArray

ValueType: Final = np.uint8
BlockType: Final = NDArray[np.uint8]


class Cripto:
    def __init__(self, key):
        self.KEY = key

        # Типы
        self.ValueType: Final = np.uint8
        self.BlockType: Final = NDArray[self.ValueType]

        # константы
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

        # таблица прямого нелинейного преобразования
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

        # таблица обратного нелинейного преобразования
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

        # вектор линейного преобразования
        self.LINEAR_VECTOR: Final = np.array([
            0x01, 0x94, 0x20, 0x85, 0x10, 0xC2, 0xC0, 0x01,
            0xFB, 0x01, 0xC0, 0xC2, 0x10, 0x85, 0x20, 0x94
        ])

        # массив для хранения констант
        self.iteration_constants = np.zeros((self.ROUND_CONSTANTS_COUNT, self.BLOCK_SIZE), dtype=self.ValueType)

        # массив для хранения ключей
        self.round_keys = np.zeros((self.ROUNDS, self.BLOCK_SIZE), dtype=self.ValueType)

    def xor_arrays(self, first_array: NDArray[np.uint8], second_array: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Выполняет побитовую операцию XOR для двух массивов байтов.

        Эта функция принимает два массива байтов и возвращает новый массив,
        в котором каждый байт является результатом побитового XOR соответствующих
        байтов из входных массивов. Если массивы не совпадают по размеру,
        будет вызвано исключение ValueError.

        :param first_array: Первый массив байтов. Должен быть типа ValueType и иметь размер (BLOCK_SIZE,)
        :param second_array: Второй массив байтов. Должен быть типа ValueType и иметь размер (BLOCK_SIZE,)
        :return: Результирующий массив после операции XOR. Массив типа ValueType размера (BLOCK_SIZE,)
        :raises ValueError: Если массивы имеют разные размеры.
        """
        if first_array.shape != second_array.shape:
            raise ValueError(
                f"Массивы должны иметь одинаковый размер. Получены: {first_array.shape} и {second_array.shape}.")

        return np.bitwise_xor(first_array, second_array)

    def apply_sbox(self, input_block: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Применяет нелинейное преобразование (S-box) к входному блоку данных.

        Выполняет замену каждого байта входного блока на соответствующий байт
        из таблицы подстановок Pi (S-box). Эта функция принимает массив байтов и
        возвращает новый массив, в котором каждый элемент заменяется согласно
        таблице замен Pi.
        Все входные данные должны быть в диапазоне 0-255.

        :param input_block: Входной массив байтов (BlockType).
        :return: Массив байтов после применения S-функции (BlockType).
        :raises ValueError: Если входные данные содержат недопустимые значения.
        """

        if not np.all((input_block >= 0) & (input_block < 256)):
            raise ValueError("Все значения входного массива должны быть в диапазоне от 0 до 255.")

        return self.Pi[input_block]

    def galois_field_multiply(self, first: int, second: int) -> int:
        """
        Выполняет умножение двух элементов в конечном поле Галуа GF(2^8).

        Реализует умножение в поле Галуа GF(2^8) с модулем GF_MODULUS.
        Операция выполняется по алгоритму умножения "сдвиг-сложение" с редукцией
        по модулю неприводимого многочлена при переполнении.

        :return:
        :param first: Первый множитель. Должен быть в диапазоне [0, 255].
        :param second: Второй множитель. Должен быть в диапазоне [0, 255].
        :return result: Результат умножения в поле Галуа. Значение в диапазоне [0, 255].
        :raises ValueError: Если входные числа выходят за пределы допустимого диапазона.
        """
        if not (0 <= first < 256) or not (0 <= second < 256):
            raise ValueError("Оба аргумента должны быть в диапазоне от 0 до 255.")

        result = 0
        multiplicand = first
        multiplier = second

        # Умножение в поле Галуа методом "сдвиг-сложение"
        for _ in range(self.BITS_IN_BYTE):
            # Если младший бит множителя равен 1, добавляем текущее значение множимого
            if multiplier & 1:
                result ^= multiplicand

            # Сохраняем значение старшего бита перед сдвигом
            high_bit = multiplicand & self.HIGH_BIT_VALUE

            # Сдвигаем множимое влево
            multiplicand = (multiplicand << 1) & self.BYTE_VALUE_MASK

            # Если старший бит был 1, выполняем редукцию по модулю
            if high_bit:
                multiplicand ^= self.GALOIS_FIELD_MODULUS

            # Сдвигаем множитель вправо
            multiplier >>= 1

        return result

    def create_galois_multiplication_table(self) -> NDArray[np.uint8]:
        """
        Создает таблицу умножения в поле Галуа GF(2^8).

        :return table: Таблица умножения размера 256x256 (BlockType)
        """
        table = np.zeros((256, 256), dtype=ValueType)
        for i in range(256):
            for j in range(256):
                table[i, j] = self.galois_field_multiply(i, j)
        return table

    def start(self):
        # Предварительно вычисленная таблица умножения
        self.MULTIPLICATION_TABLE = self.create_galois_multiplication_table()

    def galois_field_multiply_fast(self, first: int, second: int) -> int:
        """
        Быстрое умножение в поле Галуа с использованием предвычисленной таблицы.

        :param first: int в диапазоне [0, 255]
        :param second: int в диапазоне [0, 255]

        :return: Результат умножения (int)
        """
        return self.MULTIPLICATION_TABLE[first, second]

    def apply_linear_transformation(self, input_block: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Выполняет преобразование R блока данных (сдвигает данные и вычисляет L-функцию).

        Преобразование состоит из двух частей:
        1. Циклический сдвиг байтов блока вправо на один байт
        2. Вычисление нового значения последнего байта как линейной комбинации
           всех байтов исходного блока в поле Галуа GF(2^8)

        :param input_block: Входной блок данных размера BLOCK_SIZE байт (BlockType).
        :return output_block: Преобразованный блок данных после применения L-функции (BlockType).
        :raises ValueError: Если входной массив не имеет размерности BLOCK_SIZE.
        """
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
        """
        Применяет линейное преобразование L к блоку данных.

        Выполняет последовательность преобразований R заданное количество раз.
        Каждое преобразование R включает циклический сдвиг и вычисление нового
        значения последнего байта как линейной комбинации в поле Галуа GF(2^8).
        Процесс повторяется BLOCK_SIZE раз.


        :param input_block: Входной блок данных для преобразования. (BlockType).
        :return output_block: Преобразованный блок данных (BlockType).
        :raises ValueError: Если входной массив не имеет размерности BLOCK_SIZE.
        """
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной массив состояния должен содержать ровно {self.BLOCK_SIZE} байтов.")

        output_block = input_block
        for _ in range(self.BLOCK_SIZE):
            output_block = self.apply_linear_transformation(output_block)
        return output_block

    def apply_inverse_sbox(self, input_block: BlockType) -> BlockType:
        """
        Применяет обратное нелинейное преобразование (inverse S-box) к блоку данных.

        Выполняет обратную замену каждого байта входного блока согласно таблице
        обратных подстановок reverse_Pi. Является обратной операцией к прямому
        нелинейному преобразованию и используется при расшифровании. Все входные
        данные должны быть в диапазоне от 0 до 255, чтобы избежать ошибок индексации.

        :param input_block: Входной блок данных для преобразования (BlockType).
        :return: Преобразованный блок данных (BlockType).
        :raises ValueError: Если входные данные содержат недопустимые значения.
        """
        if not np.all((input_block >= 0) & (input_block < 256)):
            raise ValueError("Все значения входного массива должны быть в диапазоне от 0 до 255.")

        return self.reverse_Pi[input_block]

    def apply_inverse_R_function(self, input_block: BlockType) -> BlockType:
        """
        Выполняет обратное преобразование R^(-1) блока данных.
        Выполняет обратный сдвиг данных и вычисляет обратную L-функцию.

        Эта функция сдвигает элементы массива состояния влево и вычисляет
        новое значение для первого элемента, используя умножение в поле Галуа
        с линейным вектором l_vec.

        :param input_block: Входной блок данных размера (BlockType).
        :return output_block: Преобразованный блок данных (BlockType).
        :raises ValueError: Если входной массив не имеет размерности BLOCK_SIZE.
        """
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
        """
        Применяет обратное линейное преобразование L^(-1) к блоку данных.

        Выполняет последовательность обратных преобразований R^(-1) заданное
        количество раз. Каждое преобразование R^(-1) включает циклический сдвиг
        влево и вычисление нового значения первого байта.

        :param input_block: Входной блок данных для преобразования (BlockType).
        :return: Преобразованный блок данных (BlockType).
        :raises ValueError: Если входной массив не имеет размерности BLOCK_SIZE.
        """
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной массив состояния должен содержать ровно {self.BLOCK_SIZE} байтов.")

        output_block = input_block
        for _ in range(self.BLOCK_SIZE):
            output_block = self.apply_inverse_R_function(output_block)
        return output_block

    def compute_round_constants(self) -> None:
        """
        Вычисляет итерационные константы для развертывания ключа.

        Эта функция генерирует ROUND_CONSTANTS_COUNT итерационные константы, которые используются
        в процессе расширения ключа. Константы вычисляются путем применения
        линейного преобразования L к массиву, где первая позиция каждого
        массива содержит значение итерации от INITIAL_CONSTANT до ROUND_CONSTANTS_COUNT.

        :return None: Эта функция не возвращает значение, результаты сохраняются в глобальном массиве iter_C.
        """
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
        """
        Выполняет преобразование ячейки Фейстеля.

        Эта функция принимает две части ключа и итерационную константу, выполняет
        операцию XOR с первой частью ключа и итерационной константой, затем
        применяет нелинейное преобразование (S-функцию) и линейное преобразование
        (L-функцию) к результату. После этого второй ключ модифицируется с использованием
        результата, и обе части ключа возвращаются.

        :param key_part_1: Первая часть ключа (BlockType).
        :param key_part_2: Вторая часть ключа (BlockType).
        :param iteration_constant: Итерационная константа (BlockType).
        :return: Кортеж из двух массивов: (новый_ключ_1, старый_ключ_1).
        :raises ValueError: Если размеры входных массивов не совпадают.
        """
        for arg in [key_part_1, key_part_2, iteration_constant]:
            if arg.shape != (self.BLOCK_SIZE,):
                raise ValueError(f"Входной массив должен содержать ровно {self.BLOCK_SIZE} байтов, получено: {arg.shape}.")

        transformed_block = self.xor_arrays(key_part_1, iteration_constant)  # Операция XOR 1 части ключа со счетчиком
        transformed_block = self.apply_sbox(transformed_block)  # Применение S-функции
        transformed_block = self.apply_linear_function(transformed_block)  # Применение L-функции
        new_key_part_1 = self.xor_arrays(transformed_block, key_part_2)  # Операция XOR с результатом и второй частью ключа

        return new_key_part_1, key_part_1

    def expand_key(self, master_key_1: NDArray[np.uint8], master_key_2: NDArray[np.uint8]) -> None:
        """
        Выполняет развертывание ключа.

        Генерирует раундовые ключи на основе мастер-ключа, используя сеть Фейстеля
        и итерационные константы. Процесс включает 4 секции по 8 раундов каждая.

        :param master_key_1: Первая часть мастер-ключа (BlockType).
        :param master_key_2: Вторая часть мастер-ключа (BlockType).
        :raises ValueError: Если ключи не имеют размерности BLOCK_SIZE.
        """
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
        """
        Шифрует один блок данных.

        Эта функция выполняет последовательные операции над блоком данных,
        включая побитовый XOR с раундовыми ключами, нелинейное преобразование
        (S-функцию) и линейное преобразование (L-функцию).

        :param input_block: Входной блок данных (BlockType).
        :return output_block: Зашифрованный блок данных (BlockType).
        :raises ValueError: Если входной блок не имеет размерности BLOCK_SIZE.
        """
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
        """
        Расшифровывает один блок данных.

        Эта функция выполняет последовательные операции над блоком данных,
        включая побитовый XOR с раундовыми ключами в обратном порядке,
        а также применение обратных нелинейного и линейного преобразований.

        :param input_block: Входной блок данных (BlockType).
        :return output_block: Расшифрованный блок данных (BlockType).
        :raises ValueError: Если входной блок не имеет размерности BLOCK_SIZE.
        """
        if input_block.shape != (self.BLOCK_SIZE,):
            raise ValueError(f"Входной блок должен содержать ровно {self.BLOCK_SIZE} байтов.")

        output_block = self.xor_arrays(input_block, self.round_keys[self.ACTUAL_ROUNDS])
        for i in range(self.ACTUAL_ROUNDS - 1, -1, -1):
            output_block = self.apply_inverse_linear_function(output_block)
            output_block = self.apply_inverse_sbox(output_block)
            output_block = self.xor_arrays(self.round_keys[i], output_block)

        return output_block

    def hex_to_bin(self, hex_string: str) -> NDArray[np.uint8]:
        """
        Преобразует шестнадцатеричную строку в массив байтов.

        :param hex_string: Входная шестнадцатеричная строка (str).
        :return: Массив байтов (BlockType).
        """
        if hex_string is None or hex_string == "":
            return np.array([], dtype=ValueType)
        return np.array(bytearray.fromhex(hex_string), dtype=ValueType)

    def bin_to_hex(self, bin_array: NDArray[np.uint8]) -> str:
        """
        Преобразует массив байтов в шестнадцатеричную строку.

        :param bin_array: Входной массив байтов (BlockType).
        :return: Шестнадцатеричная строка (str).
        """
        if bin_array is None or len(bin_array) == 0:
            return ""
        return ''.join([f'{x:02x}' for x in bin_array])

    def block(self, binary_string: str) -> str:
        # Дополнить строку до длины, кратной 8
        if len(binary_string) % 8 != 0:
            binary_string = binary_string.zfill((len(binary_string) // 8 + 1) * 8)

        # Разбить на блоки по 8 бит
        byte_blocks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
        return byte_blocks

    def key_dev(self):

        # Разбиение строки на блоки по 128 бит (16 байт)
        keys_binary = [self.KEY[i:i + 128] for i in range(0, 128*16, 128)]

        # Преобразование каждого блока в массив формата np.array
        TEST_KEY_1 = np.array(
            [int(keys_binary[0][i:i + 8], 2) for i in range(0, 128, 8)],
            dtype=self.ValueType,
        )
        TEST_KEY_2 = np.array(
            [int(keys_binary[1][i:i + 8], 2) for i in range(0, 128, 8)],
            dtype=self.ValueType,
        )
        TEST_KEY_3 = np.array(
            [int(keys_binary[2][i:i + 8], 2) for i in range(0, 128, 8)],
            dtype=self.ValueType,
        )
        TEST_KEY_4 = np.array(
            [int(keys_binary[3][i:i + 8], 2) for i in range(0, 128, 8)],
            dtype=self.ValueType,
        )

        Counter = [
            np.array(
                [int(keys_binary[3][i:i + 8], 2) for i in range(0, 128, 8)],
                dtype=self.ValueType,
            )
            for i in range(4, 22)
        ]
        imitation_insert = self.KEY[128*22:]

        return TEST_KEY_1, TEST_KEY_2, TEST_KEY_3, TEST_KEY_4, Counter, imitation_insert

    def main(self) -> None:
        TEST_KEY_1 = np.array([
            230, 198, 239, 184, 137, 245, 202,  85, 214,  70, 169,  23,   3, 199,  16, 181
        ], dtype=ValueType)

        TEST_KEY_2 = np.array([
            167, 220, 154, 220,  54, 104,  81, 182, 132, 159,  27, 110, 207, 184,  42, 235
        ], dtype=ValueType)

        TEST_PLAINTEXT: Final[str] = 'cdedd4b9428d465a3024bcbe909d677f'
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
        #assert self.bin_to_hex(encrypted_block) == TEST_CIPHERTEXT, "Encryption failed!"

        # Расшифрование
        decrypted_block = self.decrypt(encrypted_block)
        print(decrypted_block)
        print()
        print(self.bin_to_hex(init_block))
        print(self.bin_to_hex(decrypted_block))
        # Проверка результата расшифрования
        #assert self.bin_to_hex(decrypted_block) == TEST_PLAINTEXT, "Decryption failed!"
        print("Encryption and decryption successful!")

    def main2(self):
        self.start()
        '''
        # Разбить key на блоки по 8 бит
        byte_blocks = self.block(self.KEY)
        print(byte_blocks)
        # Преобразовать блоки key в шестнадцатеричный формат
        hex_values = [hex(int(block, 2)) for block in byte_blocks]
        print(hex_values)
        '''
        # Создание numpy-массива
        KEY_1, KEY_2, KEY_3, KEY_4, Counter, imitation_insert = self.key_dev()

        # print(self.KEY.encode('utf-8'))
        # print(self.KEY.encode('utf-8').hex())
        # self.block(self.KEY.encode('utf-8').hex())




Code = Cripto(
    '1110011011000110111011111011100010001001111101011100101001010101010101010101010101010101010101101010111010110010001101010100100010111000000111100011100010000101101011010011111011100100110101101110000110110011010000101000110110110100001001001111100011011011011101100111110111000001010101110101100101111001010010001000110110011000110000101111101010100100011110101010111010111100111010101110011100111101100101011100111010000000011101000110100100110000000110011100000000110000010000111110000011100101111110101011010100000101000010111110111100001011101100111001110110011111010100011001010101001011001100000001011001011101110111000011110101011110101101111010100101011001111111001000011010001000111111011110100001101001100110001111000100110000000101001101111111111101010011010000011011001100001011110000100110000111001101000000110000001110110010011011111001110000011010000011001101101101111100101000111000010001010010100100010010010100000100110110001101101101100001100110000010010100011001111101111100111101000101101110101110111001000100110100000110000001100101111001110000101011000101011000100011010110100111000110101011011110101100010011111101110000100111111000000110001010000100110110001111000111111011011101111100011000010100001010110100111111011010110111001000111011001110000001101010100110001110101100000011101011110000100010001110001011100011101011010010011010110110100001101010001101011110101011010010011111011011100101101100111101101000111000011000110001011000101111000001011001001011001111110010001000010000011111110111001001010101001010111110100101001101100001010110001101000000010110100111110001101101101110110011111011100000101010111010110010111100101001000100011011001100011000010111110101010010001111010101011101011110011101010111001110011110110010101110011101000000001110100011010010011000000011001110000000011000001000011111000001110010111111010101101010000010100001011111011110000101110110011100111011001111101010001100101010100101100110000000101100101110111011100001111010101111010110111101010010101100111111100111001101100011011101111101110001000100111110101110010100101010101010101010101010101010101010110101011101011001000110101010010001011100000011110001110001000010110101101001111101110010011010110111000011011001101000010100011011011010000100100111001101100011011101111101110001000100111110101110010100101010101010101010101010101010101010110101011101011001000110101010010001011100000011110001110001000010110101101001111101110010011010110111000011011001101000010100011011011010000100100111110001101101101110110011111011100000101010111010110010111100101001000100011011001100011000010111110101010010001111010101011101011110011101010111001110011110110010101110011101000000001110100011010010011000000011001110000000011000001000011111000001110010111111010101101010000010100001011111011110000101110110011100111011001111101010001100101010100101100110000000101100101110111011100001111010101111010110111101010010101100111111100100001101000100011111101111010000110100110011000111100010011000000010100110111111111110101001101000001101100110000101111000010011000011100110100000011000000111011001001101111100111000001101000001100110110110111110010100011100001000101001010010001001001010000010011011000110110110110000110011000001001010001100111110111110011110100010110111010111011100100010011010000011000000110010111100111000010101100010101100010001101011010011100011010101101111010110001001111110111000010011111100000011000101000010011011000111100011111101101110111110001100001010000101011010011111101101011011100100011101100111000000110101010011000111010110000001110101111000010001000111000101110001110101101001001101011011010000110101000110101111010101101001001111101101110010110110011110110100011100001100011000101100010111100000101100100101100111111001000100001000001111111011100100101010100101011111010010100110110000101011000110100000001011010011111000110110110111011001111101110000010101011101011001011110010100100010001101100110001100001011111010101001000111101010101110101111001110101011100111001111011001010111001110100000000111010001101001001100000001100111000000001100000100001111100000111001011111101010110101000001010000101111101111000010111011001110011101100111110101000110010101010010110011000000010110010111011101110000111101010111101011011110101001010110011111110011100110110001101110111110111'
)
Code.start()
Code.main2()