import socket
import struct


loaded_modules = []


def load_module(name, code):
    exec code
    loaded_modules.append(name)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5555)
sock.connect(server_address)

while True:
    length = struct.unpack(">I", sock.recv(4))[0]
    message = sock.recv(length)

    cmd, _, action = message.partition(' ')

    if cmd == "load":
        name = action.split("global ")[1].split("\n")[0]
        load_module(name, action)
        print("Module %s Loaded" % name)

    elif cmd in loaded_modules:
        if action:
            exec("%s('%s')" % (cmd, action))
        else:
            exec("%s()" % cmd)
    else:
        print("Not Found: ", cmd)

    print("Loaded Modules: %s" % loaded_modules)



