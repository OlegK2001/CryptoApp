import requests
from GOST import Cripto
from flask import       \
    Flask,              \
    Blueprint,          \
    request,            \
    jsonify,            \
    render_template,    \
    request
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)
cripto = Cripto()
cripto.start()
# Адрес для пересылки сообщений
FORWARD_URL = "https://vkr.npi24.keenetic.link"  # Замените на нужный URL