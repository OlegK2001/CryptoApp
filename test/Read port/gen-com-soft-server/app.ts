import express from 'express';
import cors from 'cors';
import * as bodyParser from 'body-parser';
import {Server} from 'socket.io';
import http from 'http';
import {ReadPort} from "./src/ReadPort";

const app = express();

const server = http.createServer(app);

// Инициализация Socket.IO
const io = new Server(server, {
    cors: {
        origin: "*"
    }
});

// Обрабатываем подключение клиентов по вебсокету
io.on('connection', (socket) => {
    console.log('Клиент подключен: ', socket.id);
    // Обрабатываем отключение клиентов по вебсокету
    ReadPort(io)
    socket.on('disconnect', () => {
        console.log('Клиент отключен: ', socket.id);
    });
});

// Middleware для CORS
app.use(cors());

// Middleware для обработки JSON-запросов
app.use(bodyParser.json());

const port = process.env.PORT || 3001;
app.listen(port, () => {
    // sequelizeDataBase()
    console.log(`Сервер запущен на порту ${port}`);
});
// Запускаем сервер
server.listen(8999, () => console.log('Сервер sockets запущен на порту 8999'));

