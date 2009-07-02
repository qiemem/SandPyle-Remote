from socket import *

class CommandError(Exception):
    def __init__(self, message):
        self.msg = message
    def __str__(self):
        return self.msg

class SandpileRemote:
    def __init__(self):
        self.autoRepaint = True
        self.verbose = False
        self.echo = False

    def printVerbose(self, msg):
        if self.verbose:
            print(msg)

    def checkResult(self, result):
        if(result != "done\n"):
            raise CommandError(result)

    def tryRepaint(self):
        if(self.autoRepaint):
            self.repaint()

    def connect(self, host="localhost", port=7236):
        self.s = socket()
        self.printVerbose("Attempting to connect")
        self.s.connect((host, port))
        self.printVerbose("Connected")
        self.f = self.s.makefile()

    def close(self):
        self.s.close()
        self.f.close()

    def send(self,msg):
        if self.echo:
            self.printVerbose("Sending message: \"" + msg +"\"")
        else:
            self.printVerbose("Sending message")
        self.s.send(msg+"\n")
        self.printVerbose("Message sent")

    def receive(self):
        self.printVerbose("Waiting for message")
        msg = self.f.readline()
        if self.echo:
            self.printVerbose("Received message: \"" + msg +"\"")
        else:
            self.printVerbose("Received message")
        return msg

    def repaint(self):
        self.send("repaint")
        self.checkResult(self.receive())

    def update(self):
        self.send("update")
        self.checkResult(self.receive())
        self.tryRepaint()

    def stabilize(self):
        self.send("stabilize")
        self.checkResult(self.receive())
        self.tryRepaint()

    def deleteGraph(self):
        self.send("delete_graph")
        self.checkResult(self.receive())

    def clearSand(self):
        self.send("clear_sand")
        self.checkResult(self.receive())

    def getVertices(self):
        self.send("get_vertices")
        vertexData = self.receive()
        if vertexData == "\n":
            return []
        else:
            return map(lambda x : map(float, x.split(" ")), vertexData.split(","))

    def getEdge(self):
        self.send("get_edges")
        edgeData = self.receive()
        


