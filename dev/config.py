from dev.Modules.Cripto.GOST import Cripto
from flask import Flask, Blueprint, request, render_template, jsonify
from flask_cors import CORS
from dev.Modules.Cripto.Bin_key import key
import requests
from dev.Modules.Restoration.RideSolomon import RestorationKey

app = Flask(__name__, template_folder='templates')
CORS(app)

# инициализация модуля шифрования
cripto = Cripto()
cripto.start()
cripto.KEY = key
cripto.key_dev()

# инициализация модуля восстановления ключа
restore_key = RestorationKey()

# Адрес для пересылки сообщений
FORWARD_URL = "https://vkr.npi24.keenetic.link"  # Замените на нужный URL


messages_list = []