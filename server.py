import socket
import struct
import threading


class PayloadServer(threading.Thread):
    def __init__(self, port, address="0.0.0.0"):
        super(PayloadServer, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('0.0.0.0', port))
        self.s.listen(1)
        print("Listening on %s:%s" % (address, port))

    def run(self):
        while True:
            conn, addr = self.s.accept()  # Blocking
            data = (open("client.py").read())
            msg = struct.pack(">I", len(data)) + data
            conn.sendall(msg)


class ClientServer(threading.Thread):
    def __init__(self, port, address="0.0.0.0"):
        super(ClientServer, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('0.0.0.0', port))
        self.s.listen(1)
        print("Listening on %s:%s" % (address, port))

    def run(self):
        while True:
            conn, addr = self.s.accept()  # Blocking

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

threads = []
threads.append(PayloadServer(9999, address="localhost"))
threads.append(ClientServer(5555, address="localhost"))

for thread in threads:
    thread.start()

while True:
    try:
        pass
    except KeyboardInterrupt:
        for thread in threads:
            pass  # Kill Threads Here




