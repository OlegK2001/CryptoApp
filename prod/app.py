from config import app
from routing import routing_map

app.register_blueprint(routing_map)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




