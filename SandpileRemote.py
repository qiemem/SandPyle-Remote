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
            print(result)
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
            return map(lambda x : map(float, x.split(",")), vertexData.split(" "))

    def getVertex(self, vert):
        self.send("get_vertex "+str(vert))
        return map(float, self.receive().split(","))

    def addVertices(self, vertexPositions):
        if(len(vertexPositions)>1):
            self.send("add_vertices "+self.formatSeqOfSeqs(vertexPositions))
        else:
            self.send("add_vertices " + firstVert)
        self.checkResult(self.receive())
        self.tryRepaint()

    def addVertex(self, x, y):
        self.send("add_vertex " + str(x) + " " + str(y))
        self.checkResult(self.receive())
        self.tryRepaint()
           
    def getEdges(self):
        self.send("get_edges")
        edgeData = self.receive()
        if edgeData == "\n":
            return []
        else:
            return map(lambda x : map(int, x.split(",")), edgeData.split(" "))

    def addEdge(self, sourceVert, destVert, weight):
        self.send("add_edge "+str(sourceVert)+" "+str(destVert)+" "+str(weight))
        self.checkResult(self.receive())
        self.tryRepaint()

    def addEdges(self, edgeData):
        self.send("add_edges " + self.formatSeqOfSeqs(edgeData))
        self.checkResult(self.receive())
        self.tryRepaint()

    def getConfig(self):
        self.send("get_config")
        configData = self.receive()
        if configData == "\n":
            return []
        else:
            return map(int, configData.split(","))

    def getSand(self, vert):
        self.send("get_sand "+str(vert))
        return int(self.receive())

    def setSand(self, vert, amount):
        self.send("set_sand "+str(vert)+" "+str(amount))
        self.checkResult(self.receive())
        self.tryRepaint()

    def addSand(self, vert, amount):
        self.send("add_sand "+str(vert)+" "+str(amount))
        self.checkResult(self.receive())
        self.tryRepaint()

    def addRandomSand(self, amount):
        self.send("add_random "+str(amount))
        self.checkResponse()
        
    def setConfig(self, config):
        self.send("set_config "+self.formatSeq(config))
        self.checkResult(self.receive())
        self.tryRepaint()

    def addConfig(self, config):
        self.send("add_config "+self.formatSeq(config))
        self.checkResult(self.receive())
        self.tryRepaint()

    def getUnstables(self):
        self.send("get_unstables")
        return map(int, self.receive().split(","))

    def getNumUnstables(self):
        self.send("get_num_unstables")
        return int(self.receive())

    def isSink(self, vert):
        self.send("is_sink "+str(vert))
        response = self.receive()
        if(response=="true"):
            return True
        else:
            return False

    def getSinks(self):
        self.send("get_sinks")
        return map(int, self.receive().split(","))

    def getNonsinks(self):
        self.send("get_nonsinks")
        return map(int, self.receive().split(","))

    def getSelected(self):
        self.send("get_selected")
        return map(int, self.receive().split(","))

    def getConfigNamed(self, name):
        self.send("get_config "+name)
        return map(int, self.receive().split(","))
    
    def setToMaxStable(self):
        self.send("set_to_max_stable")
        self.checkResponse()
        self.tryRepaint()

    def addMaxStable(self):
        self.send("add_max_stable")
        self.checkResponse()
        self.tryRepaint()

    def getMaxStable(self):
        self.send("get_max_stable")
        return map(int, self.receive().split(","))

    def setToIdentity(self):
        self.send("set_to_identity")
        self.checkResponse()
        self.tryRepaint()

    def addIdentity(self):
        self.send("add_identity")
        self.checkResponse()
        self.tryRepaint()

    def getIdentity(self):
        self.send("get_identity")
        return map(int, self.receive().split(","))

    def setToBurning(self):
        self.send("set_to_burning")
        self.checkResponse()
        self.tryRepaint()

    def addBurning(self):
        self.send("add_burning")
        self.checkResponse()
        self.tryRepaint()

    def getBurning(self):
        self.send("get_burning")
        return map(int, self.receive().split(","))

    def setToDual(self):
        self.send("set_to_dual")
        self.checkResponse()
        self.tryRepaint()

    def addDual(self):
        self.send("add_dual")
        self.checkResponse()
        self.tryRepaint()

    def getDual(self):
        self.send("get_dual")
        return map(int, self.receive().split(","))


    def formatSeq(self, seq):
        return reduce(lambda s, x : s+","+str(x), seq[1:], str(seq[0]))
    
    def formatSeqOfSeqs(self, seq):
        return reduce(lambda s, x : s+" "+self.formatSeq(x), seq[1:], self.formatSeq(seq[0]))

    
