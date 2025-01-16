import requests
import serial
from threading import Thread, Event
import logging
key = ''

# Настройки для портов
port_settings = {
    'port1': {'path': 'COM3', 'baudrate': 38400},
    'port2': {'path': 'COM4', 'baudrate': 38400}
}

# Глобальные переменные для потоков и статусов портов
threads = {}
stop_events = {}

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_port(port_name, io):
    """Инициализация последовательного порта и обработка данных."""
    settings = port_settings.get(port_name)
    if not settings:
        logging.error(f"Нет настроек для порта {port_name}")
        return

    try:
        # Открываем последовательный порт
        port = serial.Serial(settings['path'], baudrate=settings['baudrate'], timeout=1)
        logging.info(f"{port_name} открыт: {settings['path']}")

        # Отправляем событие о подключении
        io.emit(port_name, {'status': 'connect', 'data': ''})

        # Событие для остановки потока
        stop_event = Event()
        stop_events[port_name] = stop_event

        # Читаем данные из порта
        def read_from_port():
            global key
            while not stop_event.is_set():
                try:
                    data = port.readline().decode('utf-8').strip()
                    key += data
                    if data:
                        io.emit(port_name, {'status': 'send', 'data': data})
                        if len(key) > 4096:
                            send_key_to_service(key)
                            del data
                except Exception as e:
                    logging.error(f"Ошибка чтения из {port_name}: {e}")
                    io.emit(port_name, {'status': 'error', 'data': str(e)})
                    break
            # Закрываем порт при завершении
            port.close()
            logging.info(f"{port_name} закрыт.")

        # Запуск чтения порта в отдельном потоке
        thread = Thread(target=read_from_port, daemon=True)
        threads[port_name] = thread
        thread.start()

    except serial.SerialException as e:
        # Если порт недоступен, отправляем ошибку
        logging.error(f"Ошибка открытия {port_name}: {e}")
        io.emit(port_name, {'status': 'error', 'data': str(e)})


def read_ports(io):
    """Инициализация всех настроенных портов."""
    for port_name in port_settings.keys():
        if port_name not in threads:  # Избегаем повторного запуска
            initialize_port(port_name, io)


def close_ports():
    """Закрытие всех активных портов."""
    for port_name, stop_event in stop_events.items():
        stop_event.set()
    for port_name, thread in threads.items():
        thread.join()
    stop_events.clear()
    threads.clear()
    logging.info("Все порты закрыты.")


def send_key_to_service(key):
    """Отправка ключа на сервер через POST-запрос."""
    try:
        url = "http://127.0.0.1:4500/api/editKey"  # Замените на актуальный адрес
        payload = {"key": key}
        headers = {"Content-Type": "application/json"}

        # Выполняем POST-запрос
        response = requests.post(url, json=payload, headers=headers)

        # Проверяем статус ответа
        if response.status_code == 200:
            return {"status": "success", "message": response.json()}
        else:
            return {"status": "error", "message": response.text}

    except requests.RequestException as e:
        return {"status": "error", "message": str(e)}
