from socket import *

class CommandError(Exception):
    def __init__(self, message):
        self.msg = message
    def __str__(self):
        return self.msg

class SandpileRemote:
    def __init__(self):
        self.autoRepaint = True

    def checkResult(self, result):
        if(result != "done\n"):
            raise CommandError(result)

    def tryRepaint(self):
        if(self.autoRepaint):
            self.repaint()

    def connect(self, host="localhost", port=7236):
        self.s = socket()
        self.s.connect((host, port))

    def close(self):
        self.s.close()

    def repaint(self):
        self.s.send("repaint\n")
        self.checkResult(self.s.recv(2048))

    def update(self):
        self.s.send("update\n")
        self.checkResult(self.s.recv(2048))
        self.tryRepaint()


