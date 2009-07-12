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
        indexEdgeData = map(lambda e : (labelsToIndices[e[0]], labelsToIndices[e[1]], e[2]), edgeData)
        self.srem.addEdges(indexEdgeData)

    def getConfig(self):
        config = self.srem.getConfig()
        labelledConfig = {}
        for i in range(len(config)):
            labelledConfig[self.indicesToLabels[i]] = config[i]
        return labelledConfig

    def getSand(self, vert):
        return self.srem.getSand(self.labelsToIndices[vert])

    def setSand(self, vert, amount):
        self.srem.setSand(labelsToIndices[vert], amount)

    def addSand(self, vert, amount):
        r"""
        Adds the amount of sand to the indicated vertex.

        INPUT:

        ``vert`` - the label of the vertex

        ``amount`` - int; the number of grains to add.

        OUTPUT:

        None

        NOTES:

        ``amount`` can be negative, thus removing sand from the vertex.
          If the number of grains on the vertex drops below 0, it will
          stay there; thus the vertex will sort of be in debt.

        EXAMPLES::
        """
        self.srem.addSand(labelsToIndices[vert])

    def addRandomSand(self, amount):
        r"""
        Adds random sand to the nonsink vertices.

        INPUT:

        ``amount`` - int; the total number of grains to add.

        OUTPUT:

        None

        NOTES:

        If ``amount`` is negative, no sand will be added or taken away.

        EXAMPLES::
        """
        self.srem.addRandomSand(amount)
        
    def setConfig(self, config):
        r"""
        Sets the current configuration in the program.

        INPUT:

        ``config`` - A dictionary mapping labels to integers.

        OUTPUT:

        None

        NOTES:

        Negative amounts of sand are allowed.

        EXAMPLES::
        """
        self.srem.setConfig(self.__labelledConfigToIndexed(config))

    def addConfig(self, config):
        r"""
        Adds the given configuration to the current configuration in the program.

        INPUT:

        ``config`` - A dictionary mapping labels to integers

        OUTPUT:

        None

        NOTES:

        Negative amounts of sand are allowed.

        EXAMPLES::
        """
        self.srem.addConfig(self.__labelledConfigToIndexed(config))

    def getUnstables(self):
        r"""
        Gets a list of the unstable vertices.

        INPUT:

        None

        OUTPUT:

        A list of labels that are the indices of the unstables vertices.

        NOTES:

        Should never return sinks.

        EXAMPLES::
        """
        return self.__indexedVerticesToLabelled(self.srem.getUnstables())

    def getNumUnstables(self):
        r"""
        Returns the number of unstable vertices.

        INPUT:

        None

        OUTPUT:

        int; the number of unstable vertices.

        NOTES:

        This is very useful collecting the number of firings during
          a stabilization. See the example.

        EXAMPLES::
        """
        return self.__indexedVerticesToLabelled(self.srem.getUnstables())

    def isSink(self, vert):
        r"""
        Tells whether or the indicated vertex is a sink.

        INPUT:

        ``vert`` - The label of the vertex.

        OUTPUT:

        boolean; True means that the vertex is a sink.

        EXAMPLES::
        """ 
        return self.srem.isSink(self.labelsToIndices[vert])

    def getSinks(self):
        r"""
        Returns a list of all the sinks.

        INPUT:

        None
      
        OUTPUT:
        
        A list of the labels of the sinks.

        EXAMPLES::
        """
        return self.__

    def getNonsinks(self):
        r"""
        Returns a list of all the sinks.

        INPUT:

        None
      
        OUTPUT:
        
        A list of the indices (ints) of the sinks.

        EXAMPLES::
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0], [10.0, 0]])
            >>> srem.addEdges([[0, 1, 1], [1, 0, 10], [1, 10, 10]])
            >>> srem.getSinks()
                [0, 1]
        """
        self.send("get_nonsinks")
        return map(int, self.receive().split(","))

    def getSelected(self):
        r"""
        Returns a list of all the vertices that are currently
          selected in the program.

        INPUT:

        None

        OUTPUT:

        A list of the indices (ints) of the selected vertices.

        EXAMPLES::

        Suppose we select the middle four vertices of a 20x20 grid 
          with sinks around the edges. Then we have:
        
        >>> srem.getSelected()
            [189, 190, 210, 209]
        """
        self.send("get_selected")
        return map(int, self.receive().split(","))

    def getConfigNamed(self, name):
        r"""
        Returns the configuration store in the config manager of
          the program with under the given name.
        
        INPUT:

        ``name`` - string; The name of the configuration

        OUTPUT:

        The configuration as a list of integers representing the
          amount of sand at each vertex.

        NOTES:

        Currently, only custom configs and identity can be returned
          this way. Max stable, burning, etc. have their own functions.

        EXAMPLES::

        If you have stored configuration named "Config", then you would
          use
          
            >>> srem.getConfigNames("Config")
        """

        self.send("get_config "+name)
        return map(int, self.receive().split(","))
    
    def setToMaxStable(self):
        r"""
        Sets the current configuration to the max stable configuration.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.setToMaxStable()
        """

        self.send("set_to_max_stable")
        self.__checkResult()
        self.__tryRepaint()

    def addMaxStable(self):
        self.send("add_max_stable")
        self.__checkResult()
        self.__tryRepaint()

    def getMaxStable(self):
        self.send("get_max_stable")
        return map(int, self.receive().split(","))

    def setToIdentity(self):
        r"""
        Sets the current configuration to the identity configuration.

        INPUT:

        None

        OUTPUT:

        None

        NOTES:

        Calculating the identity can take a long time on big graphs
          but then is automatically stored for later use. However,
          if the graph is changed, the identity will have to be
          recalculated.

        EXAMPLES::

            >>> srem.setToIdentity()
        """
        self.send("set_to_identity")
        self.__checkResult()
        self.__tryRepaint()

    def addIdentity(self):
        r"""
        Adds the identity configuration to the current configurationXS.

        INPUT:

        None

        OUTPUT:

        None

        NOTES:

        Calculating the identity can take a long time on big graphs
          but then is automatically stored for later use. However,
          if the graph is changed, the identity will have to be
          recalculated.

        EXAMPLES::

            >>> srem.addIdentity()
        """
        self.send("add_identity")
        self.__checkResult()
        self.__tryRepaint()

    def getIdentity(self):
        self.send("get_identity")
        return map(int, self.receive().split(","))

    def setToBurning(self):
        r"""
        Sets the current configuration to the minimal burning
          configuration.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.setToBurning()
        """
        self.send("set_to_burning")
        self.__checkResult()
        self.__tryRepaint()

    def addBurning(self):
        self.send("add_burning")
        self.__checkResult()
        self.__tryRepaint()

    def getBurning(self):
        self.send("get_burning")
        return map(int, self.receive().split(","))

    def setToDual(self):
        self.send("set_to_dual")
        self.__checkResult()
        self.__tryRepaint()

    def addDual(self):
        self.send("add_dual")
        self.__checkResult()
        self.__tryRepaint()

    def getDual(self):
        self.send("get_dual")
        return map(int, self.receive().split(","))


    def __labelledConfigToIndexed(self, config):
        return map(lambda v : config[indicesToLabels[v]], range(len(config)))

    def __indexedConfigToLabelled(self, config):
        return dict(map(lambda v : (indicesToLabels[v], config[v]), range(len(config))))

    def __labelledVerticesToIndexed(self, vertices):
        return map(lambda v : labelsToIndices[v], vertices)
    
    def __indexedVertices(self, vertices):
        return map(lambda v : indicesToLabels[v], vertices)

    
