from SandpileRemote import *

class SageRemote:

    def __init__(self):
        self.srem = SandpileRemote()
        self.labelsToIndices = dict()
        self.indicesToLabels = list()

    def connect(self, host="localhost", port=7236):
        self.srem.connect(host, port)

    def close(self):
        self.srem.close()

    def repaint(self):
        r"""
        Tells the program to repaint. The program will not repaint
        if the repaint option is off in Visual Options.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.repaint()
        """
        self.srem.repaint()

    def update(self):
        r"""
        Tells the program to fire all unstable vertices.

        INPUT:
        
        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.update()
        """
        self.srem.update()

    def stabilize(self):
        r"""
        Tells the program to stabilize the current configuration.
        Warning: If the current graph and configuration cannot stabilize
        (there is no global sink), then the program will enter an infinite
        loop and this method will never return. Also note that this can
        take a long time depending on the graph and configuration.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.stabilize()
        """
        self.srem.stabilize()

    def deleteGraph(self):
        r"""
        Tells the program to delete all vertices and edges.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.deleteGraph()
        """
        self.srem.deleteGraph()
        self.labelsToIndices = dict()
        self.indicesToLabels = list()

    def clearSand(self):
        r"""
        Sets each vertex to 0 grains of sand.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.clearSand()
        """
        self.srem.clearSand()

    def getVertices(self):
        vertDataList = self.srem.getVertices()
        vertData = dict()
        for v in labelsToIndices:
            vertData[v] = vertDataList[labelsToIndices[v]]
        return vertData

    def getVertex(self, vert):
        return self.srem.getVertex(labelsToIndices(vert))

    def addVertices(self, vertexPositions):
        posList = []
        for v in vertexPositions:
            self.labelsToIndices[v]=len(indicesToLabels)
            self.indicesToLabels.append(v)
            posList.append(vertexPositions[v])
        self.srem.addVertices(posList)

    def addVertex(self, label, x, y):
        self.labelsToIndices[label] = len(indicesToLabels)
        self.indicesToLabels.append(label)
        self.srem.addVertex(x,y)

    def addEdge(self, sourceVert, destVert, weight):
        self.srem.addEdge(labelsToIndices[sourceVert], labelsToIndices[destVert], weight)

    def addEdges(self, edgeData):
        


