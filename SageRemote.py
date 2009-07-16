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

    def getGraph(self):
        r"""
        Retrieves the current graph in the program.

        INPUT:

        None

        OUTPUT:

        A DiGraph.

        EXAMPLES::
        
        """
        self.indicesToLabels = list()
        self.labelsToIndices = dict()
        vertexPosList = self.srem.getVertices()
        sinks = set(self.srem.getSinks())
        edges = self.srem.getEdges()
        vertexPosDict = dict()
        graphData={'sink' : {}}
        for v in range(len(vertexPosList)):
            if v in sinks:
                self.indicesToLabels.append('sink')
            else:
                self.indicesToLabels.append(v)
                self.labelsToIndices[v]=v
                graphData[v] = dict()
                vertexPosDict[v]=vertexPosList[v]
        for e in edges:
            if e[1] in sinks:
                graphData[e[0]]['sink'] = e[2]
            else:
                graphData[e[0]][e[1]]=e[2]
        return DiGraph(data=graphData, pos=vertexPosDict)

    def setGraph(self, graph, scale=10.0, offset = (0.0, 0.0)):
        r"""
        Sets the programs graph to the given graph.

        INPUTS:

        graph - Anything that inherits from GenericGraph; this 
          include Graph, DiGraph, Sandpile (from David Perkinson's
          sandpile library), etc.

        OUPUTS:

        None

        EXAMPLES::

        """
        if graph.get_pos() is None:
            graph.plot(save_pos=True)
        self.labelsToIndices = dict()
        self.indicesToLabels = list()
        vertexPositions = list()
        for v in graph.vertices():
            self.labelsToIndices[v] = len(self.indicesToLabels)
            self.indicesToLabels.append(v)
            pos = graph.get_pos()[v]
            vertexPositions.append([scale * pos[0] + offset[0], scale*pos[1] + offset[1]])
        self.srem.deleteGraph()
        self.srem.addVertices(vertexPositions)
        edges = list()
        for e in graph.edges():
            edges.append([self.labelsToIndices[e[0]], self.labelsToIndices[e[1]], e[2]])
        self.srem.addEdges(edges)
            

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
        return self.__indexedVerticesToLabelled(self.srem.getSinks())

    def getNonsinks(self):
        r"""
        Returns a list of all the sinks.

        INPUT:

        None
      
        OUTPUT:
        
        A list of the labels of the sinks.

        EXAMPLES::
        """
        return self.__indexedVerticesToLabelled(self.srem.getSinks())

    def getSelected(self):
        r"""
        Returns a list of all the vertices that are currently
          selected in the program.

        INPUT:

        None

        OUTPUT:

        A list of the labels of the selected vertices.

        EXAMPLES::
        """
        return self.__indexedVerticesToLabelled(self.srem.getSelected())

    def getConfigNamed(self, name):
        r"""
        Returns the configuration store in the config manager of
          the program with under the given name.
        
        INPUT:

        ``name`` - string; The name of the configuration

        OUTPUT:

        The configuration as a dictionary from labels to ints.

        NOTES:

        Currently, only custom configs and identity can be returned
          this way. Max stable, burning, etc. have their own functions.

        EXAMPLES::
        """

        return self.__indexedConfigToLabelled(self.srem.getConfigNamed(name))
    
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

        self.srem.setToMaxStable()

    def addMaxStable(self):
        self.srem.addMaxStable()

    def getMaxStable(self):
        return self.__indexedConfigToLabelled(self.srem.getMaxStable())

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
        self.srem.setToIdentity()

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
        self.srem.addIdentity()

    def getIdentity(self):
        return self.__indexedConfigToLabelled(self.srem.getIdentity())

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
        self.srem.setToBurning()

    def addBurning(self):
        self.srem.addBurning()

    def getBurning(self):
        return self.__indexedConfigToLabelled(self.srem.getBurning())

    def setToDual(self):
        self.srem.setToDual()

    def addDual(self):
        self.srem.addDual()

    def getDual(self):
        return self.__indexedConfigToLabelled(self.srem.getDual())


    def __labelledConfigToIndexed(self, config):
        return map(lambda v : config[indicesToLabels[v]], range(len(config)))

    def __indexedConfigToLabelled(self, config):
        return dict(map(lambda v : (indicesToLabels[v], config[v]), range(len(config))))

    def __labelledVerticesToIndexed(self, vertices):
        return map(lambda v : labelsToIndices[v], vertices)
    
    def __indexedVertices(self, vertices):
        return map(lambda v : indicesToLabels[v], vertices)

    
