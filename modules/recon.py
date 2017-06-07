global Recon

global os
import os


class Recon:
    def __init__(self):
        print("OS: ", os.uname())
        print("User: ", os.getlogin())
        print("UID: ", os.getuid())



