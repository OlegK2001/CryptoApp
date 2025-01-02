from config import Blueprint, request, render_template
import service

routing_map = Blueprint('main', __name__)
# Список для хранения сообщений


@routing_map.route('/api/send', methods=['POST'])
def send_message():
    """Получение сообщения от клиента и пересылка на указанный адрес."""
    return service.send_message(request.json)


@routing_map.route(f'/api/receive', methods=['GET'])
def receive_message():
    """Получение сообщения от внешнего источника."""
    return service.receive_message()


@routing_map.route('/')
def serve_chat_page():
    """Возвращает HTML-страницу чата."""
    return render_template('index.html')

