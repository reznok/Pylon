global HelloWorld


class HelloWorld:
    def __init__(self, action=None):
        if action == "print":
            self.print_hello()
        else:
            print("Prints Hello World Message!")

    def print_hello(self):
        print("Hello There!")
