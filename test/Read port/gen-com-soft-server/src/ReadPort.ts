import {SerialPort} from "serialport";
import {ReadlineParser} from "@serialport/parser-readline";
import {Server} from "socket.io";

interface IData {
    status: 'connect' | 'send' | 'error',
    data: string | boolean
}

interface IPortSettings {
    path: string,
    baudRate: number
}

const portSettings: { [key: string]: IPortSettings } = {
    'port1': {path: '/dev/tty.usbserial-120', baudRate: 38400},
    'port2': {path: '/dev/tty.usbserial-110', baudRate: 38400}
};

const initializePort = (portName: string, io: Server) => {

    const port = new SerialPort(portSettings[portName]);
    const parser = port.pipe(new ReadlineParser({delimiter: '\r\n'}));

    port.on('open', () => {
        io.emit(portName, {
            status: 'connect',
            data: ''
        });
    });

    parser.on('data', (data) => {
        const dataString = data.toString();
        io.emit(portName, {
            status: 'send',
            data: dataString
        });
    });

    port.on('error', (err) => {
        io.emit(portName, {
            status: 'error',
            data: err.message
        });
    });
};

export const ReadPort = (io: Server) => {
    Object.keys(portSettings).forEach(portName => {
        initializePort(portName, io);
    });
};
