from config import app
from dev.Modules.Chat.routing import routing_map

app.register_blueprint(routing_map)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)




