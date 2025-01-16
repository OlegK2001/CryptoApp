import reedsolo


class RestorationKey:
    def __init__(self):
        # Задаем параметры
        self.bit_sequence_length = 4096  # Длина исходной двоичной последовательности в битах
        self.error_symbols = 80  # Количество символов (байт), которые будут заменены ошибками

        # Создаем двоичную последовательность длиной 256 бит
        self.original_bits = None
        self.decoded_bits = None
        self.rs = reedsolo.RSCodec(self.error_symbols * 2)

    def generate_bite(self):
        # Преобразуем двоичную последовательность в байты
        self.original_data = bytes(int(self.original_bits[i:i+8], 2) for i in range(0, self.bit_sequence_length, 8))

        # Создаем объект для кода Рида-Соломона с указанным количеством контрольных символов

        # Кодируем данные и сохраняем только контрольные символы
        encoded_data = self.rs.encode(self.original_data)
        self.control_symbols = encoded_data[len(self.original_data):]  # контрольные символы

    def received_key(self, control_symbols):
        received_data = bytearray(self.original_bits)

        # Объединяем искаженные данные с контрольными символами
        data_with_errors_and_controls = bytes(received_data) + control_symbols

        # Декодируем и исправляем ошибки с использованием контрольных символов
        try:
            decoded_data, _, _ = self.rs.decode(data_with_errors_and_controls)
            self.decoded_bits = ''.join(f'{byte:08b}' for byte in decoded_data)
            print("Ошибки успешно исправлены.")
        except reedsolo.ReedSolomonError as e:
            print("Не удалось исправить ошибки:", e)


