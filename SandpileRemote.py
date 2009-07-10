r"""
Sandpile Remote

A class for interacting remotely with the Sandpiles standalone program.

Version: 2009.6.7

AUTHOR:
    -- Bryan Head (2009-06-7)

EXAMPLES:

After the Sandpiles program is running, hit the "Server" button and press yes.
Then, from a Python terminal, we can create an instance of the SandileRemote class
and connect to the program:

    >>> srem = SandpileRemove()
    >>> srem.connect()

The Sandpile program will inform you of the connection.
"""

from socket import *

class CommandError(Exception):
    """
    This error should occur when the Sandpile program doesn't know
    what to do with a particular command.
    """

    def __init__(self, message):
        self.msg = message
    def __str__(self):
        return self.msg

class SandpileRemote:
    r"""
    This class can connect connect to the Sandpile program and can
    issue remote commands. Note that an instance of this class has
    several boolean fields to customize behavior:

    autoRepaint - If True, will automatically send the repaint command
    to the Sandpile program after every command that manipulates either
    the graph or configuration. Default is True.

    verbose - If True, the current operation will be printed out. Ex:
        >>> srem..update()
            Sending message
            Message sent
            Waiting for message
            Received message
            Sending message
            Message sent
            Waiting for message
            Received message
    Default is False.

    echo - If verbose is True and this is True, will print out the contents
    of each message sent and received.
        >>> srem.update()
            Sending message: "update"
            Message sent
            Waiting for message
            Received message: "done"
            Sending message: "repaint"
            Message sent
            Waiting for message
            Received message: "done"
    Warning: When dealing with such getConfig, getVertices, etc., the messages
    can be massive. It is highly recommended to have this off unless you need
    it for debugging purposes. Default is False.
    """

    def __init__(self):
        r"""
        Create an object to access the Sandpile program remotely.

        INPUT:

        None

        OUTPUT:
        
        SandpileRemote

        EXAMPLES:

        >>> srem = SandpileRemote()
        """
        self.autoRepaint = True
        self.verbose = False
        self.echo = False

    def __printVerbose(self, msg):
        """
        A convenience method. If self.verbose=True, prints msg.
        """
        if self.verbose:
            print(msg)

    def __checkResult(self, result):
        """
        Makes sure that the response issued by the Sandpile program after
        a non-get command is not an error. The Sandpile program issues the
        response "done\n" unless there is an error, or certain other data
        was requested. This just checks to make sure result == "done\n"
        and raises an exception if not.
        """
        if(result != "done\n"):
            print(result)
            raise CommandError(result)

    def __tryRepaint(self):
        """
        A convenience method that will send the repaint command if autorepaint
        is True.
        """
        if(self.autoRepaint):
            self.repaint()

    def connect(self, host="localhost", port=7236):
        r"""
        Attempts to connect to the Sandpile program. If the program is not
        accepting connections, will raise a Connection refused error.

        INPUT:
        
        - ``host`` (optional) - A string representing the host address. Default
          "localhost"

        - ``port`` (optional) - An int representing the port to use. Default is
          7236.
        
        OUTPUT:

        None

        EXAMPLES::

        Use default settings:

            >>> srem = SandpileRemote()
            >>> srem.connect()

        No other settings have been tested. To use them, do:
        
            >>> srem = SandpileRemote()
            >>> srem.connect(host="some_ip_address", port=1234)
        """
        self.s = socket()
        self.__printVerbose("Attempting to connect")
        self.s.connect((host, port))
        self.__printVerbose("Connected")
        self.f = self.s.makefile()

    def close(self):
        r"""
        Closes the current connection. Its not usually necessary
        to call this.

        INPUT:
       
        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.close()
        """
        self.s.close()
        self.f.close()

    def send(self,msg):
        r"""
        Sends a message to the program. Errors if not connected or
        if the program errors. This shouldn't typically be used by
        the user. Note that this does not flush the response buffer
        so there will be a backup of responses from the program if
        the user does not call receive().

        INPUT:

        ``msg`` - A string of the message to send. Should NOT end with '\n'.
          Otherwise the program will think its receiving multiples messages.

        OUTPUT:

        None

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.send("add_vertex 0.0 0.0")
            >>> srem.receive()
                'done\n'
            >>> srem.send("get_vertices")
            >>> srem.receive()
                '0.0,0.0\n'
        """

        if self.echo:
            self.__printVerbose("Sending message: \"" + msg +"\"")
        else:
            self.__printVerbose("Sending message")
        self.s.send(msg+"\n")
        self.__printVerbose("Message sent")

    def receive(self):
        r"""
        Receives a single message sent by the program. If none is present, 
        it will wait until there is.

        INPUT:

        None

        OUTPUT:

        string

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.send("add_vertex 0.0 0.0")
            >>> srem.receive()
                'done\n'
            >>> srem.send("get_vertices")
            >>> srem.receive()
                '0.0,0.0\n'
        """
        self.__printVerbose("Waiting for message")
        msg = self.f.readline()
        if self.echo:
            self.__printVerbose("Received message: \"" + msg +"\"")
        else:
            self.__printVerbose("Received message")
        return msg

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
        self.send("repaint")
        self.__checkResult(self.receive())

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
        self.send("update")
        self.__checkResult(self.receive())
        self.__tryRepaint()

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
        self.send("stabilize")
        self.__checkResult(self.receive())
        self.__tryRepaint()

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
        self.send("delete_graph")
        self.__checkResult(self.receive())

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
        self.send("clear_sand")
        self.__checkResult(self.receive())

    def getVertices(self):
        r"""
        Returns the positions of the vertices in the graph.

        INPUT:

        None

        OUTPUT:

        A list of lists of floats. Format: [[x1,y1], [x2,y2], ...]

        EXAMPLES::
        
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [3.0,-2.0]])
            >>> srem.getVertices()
                [[0.0, 0.0], [3.0, -2.0]]
        """
        self.send("get_vertices")
        vertexData = self.receive()
        if vertexData == "\n":
            return []
        else:
            return map(lambda x : map(float, x.split(",")), vertexData.split(" "))

    def getVertex(self, vert):
        r"""
        Returns the position of a vertex.

        INPUT:

        ``vert`` - An int representing the index of the desired vertex.

        OUTPUT:

        A list of float: [x, y].

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [3.0,-2.0]])
            >>> srem.getVertex(1)
                [3.0, -2.0]
        """
        
        self.send("get_vertex "+str(vert))
        return map(float, self.receive().split(","))

    def addVertices(self, vertexPositions):
        """
        Adds vertices at the indicated positions to the graph.

        INPUT:

        ``vertexPositions`` - A list of lists of floats of the format:
          [[x1, y1], [x2, y2],...]

        OUTPUT:

        None

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [3.0, -2.0]])
            >>> srem.addVertices([[5.0, 5.0], [1.0, 2.0]])
            >>> srem.getVertices()
                [[0.0, 0.0], [3.0, -2.0], [5.0, 5.0], [1.0, 2.0]]
        """
        if(len(vertexPositions)>1):
            self.send("add_vertices "+self.formatSeqOfSeqs(vertexPositions))
        else:
            self.send("add_vertices " + firstVert)
        self.__checkResult(self.receive())
        self.__tryRepaint()

    def addVertex(self, x, y):
        r"""
        Adds a vertex at the indicated position.

        INPUT:

        ``x`` - A float representing the x-coordinate of the vertex.
        ``y`` - A float representing the y-coordinate of the vertex.

        OUTPUT:

        None

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertex(0.0, 0.0)
            >>> srem.addVertex(5.0, 5.0)
            >>> srem.getVertices()
                [[0.0, 0.0], [5.0, 5.0]]
        """
        self.send("add_vertex " + str(x) + " " + str(y))
        self.__checkResult(self.receive())
        self.__tryRepaint()

    def getEdges(self):
        """
        Returns the edges of the current graph.

        INPUT:

        None

        OUTPUT:

        A list of lists of integers of the format: [[v1, v2, w12], [v3, v4, w34], ...]
          where v1 is the index of the source vertex, v2 is the index of destination
          vertex and w12 is the weight of the edge. Likewise for [v3, v4, w34].

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertex(0.0, 0.0)
            >>> srem.addVertex(5.0, 5.0)
            >>> srem.addEdge(0, 1, 5)
            >>> srem.getEdges()
                [[0, 1, 5]]
            >>> srem.addEdge(1, 0, 2)
            >>> srem.getEdges()
                [[0, 1, 5], [1, 0, 2]]
        """        
        self.send("get_edges")
        edgeData = self.receive()
        if edgeData == "\n":
            return []
        else:
            return map(lambda x : map(int, x.split(",")), edgeData.split(" "))

    def addEdge(self, sourceVert, destVert, weight):
        r"""
        Adds an edge to the graph.

        INPUT:

        ``sourceVert`` - An int representing the index of the source vertex.

        ``destVert`` - An int representing the index of the destination vertex.

        ``weight`` - An int representing the weight of the edge.

        OUTPUT:

        None

        NOTES:

        If there is an edge already present between ``sourceVert`` and
          ``destVert``, the weight of the edge will be increased by
          ``weight``. Thus, negative weights will decrease the weight 
          of the edge. If the weight of the edge falls to 0 or below, it 
          will be removed.

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertex(0.0, 0.0)
            >>> srem.addVertex(5.0, 5.0)
            >>> srem.addEdge(0, 1, 5)
            >>> srem.getEdges()
                [[0, 1, 5]]
            >>> srem.addEdge(1, 0, 2)
            >>> srem.getEdges()
                [[0, 1, 5], [1, 0, 2]]
            >>> srem.addEdge(0, 1, 3)
            >>> srem.getEdges()
                [[0, 1, 8], [1, 0, 2]]
            >>> srem.addEdge(1, 0, -2)
            >>> [[0, 1, 8]]
        """
        self.send("add_edge "+str(sourceVert)+" "+str(destVert)+" "+str(weight))
        self.__checkResult(self.receive())
        self.__tryRepaint()

    def addEdges(self, edgeData):
        r"""
        Adds edges to the graph.

        INPUT:

        ``edgeData`` - A list of lists of integers of the format: 
          [[v1, v2, w12], [v3, v4, w34], ...] where v1 is the index 
          of the source vertex, v2 is the index of destination vertex
          and w12 is the weight of the edge. Likewise for [v3, v4, w34].

        OUTPUT:

        None

        NOTES:

        If there is an edge already present between ``sourceVert`` and
          ``destVert``, the weight of the edge will be increased by
          ``weight``. Thus, negative weights will decrease the weight 
          of the edge. If the weight of the edge falls to 0 or below, it 
          will be removed.

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0]])
            >>> srem.addEdge([[0, 1, 5], [1, 0, 2]])
            >>> srem.getEdges()
                [[0, 1, 5], [1, 0, 2]]
            >>> srem.addEdge([[0, 1, 3], [1, 0, -2]])
            >>> srem.getEdges()
            >>> [[0, 1, 8]]
        """
        self.send("add_edges " + self.formatSeqOfSeqs(edgeData))
        self.__checkResult(self.receive())
        self.__tryRepaint()

    def getConfig(self):
        r"""
        Returns the current configuration of the graph.

        INPUT:

        None

        OUTPUT:

        A list of integers representing the amount of sand at each vertex.

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0]])
            >>> srem.setConfig([3,4])
            >>> srem.getConfig()
                [3, 4]
        """

        self.send("get_config")
        configData = self.receive()
        if configData == "\n":
            return []
        else:
            return map(int, configData.split(","))

    def getSand(self, vert):
        r"""
        Returns the amount of sand at the indicated vertex.

        INPUT:

        ``vert`` - int; the index of the vertex.

        OUTPUT:

        int; the amount of sand at vertex ``vert``.

        EXAMPLES::
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0]])
            >>> srem.getSand(1)
                0
            >>> srem.setConfig([3,4])
            >>> stem.getSand(0)
                3
            >>> stem.getSand(1)
                4
        """
        self.send("get_sand "+str(vert))
        return int(self.receive())

    def setSand(self, vert, amount):
        r"""
        Sets the amount of sand at the indicated vertex.

        INPUT:

        ``vert`` - int; the index of the vertex.

        ``amount`` - int; the number of grains.

        OUTPUT:

        None

        NOTES:

        ``amount`` can be negative, and thus makeing the vertex in debt
          so to speak.

        EXAMPLES::
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0]])
            >>> srem.setSand(1,4)
            >>> srem.getSand(1)
                4
            >>> srem.setSand(1,-7)
            >>> srem.getSand(1)
                -7
        """
        self.send("set_sand "+str(vert)+" "+str(amount))
        self.__checkResult(self.receive())
        self.__tryRepaint()

    def addSand(self, vert, amount):
        r"""
        Adds the amount of sand to the indicated vertex.

        INPUT:

        ``vert`` - int; the index of the vertex.

        ``amount`` - int; the number of grains to add.

        OUTPUT:

        None

        NOTES:

        ``amount`` can be negative, thus removing sand from the vertex.
          If the number of grains on the vertex drops below 0, it will
          stay there; thus the vertex will sort of be in debt.

        EXAMPLES::
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0]])
            >>> srem.addSand(1,4)
            >>> srem.getSand(1)
                4
            >>> srem.addSand(1,-7)
            >>> srem.getSand(1)
                -3
        """
        self.send("add_sand "+str(vert)+" "+str(amount))
        self.__checkResult(self.receive())
        self.__tryRepaint()

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
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0], [10.0, 0]])
            >>> srem.addEdges([[0,1,1],[1,0,1], [1, 2, 1]])
            >>> srem.addRandomSand(10)
            >>> srem.getConfig()
                [3, 7, 0]
        """
        self.send("add_random_sand "+str(amount))
        self.__checkResult(self.receive())
        self.__tryRepaint()
        
    def setConfig(self, config):
        r"""
        Sets the current configuration in the program.

        INPUT:

        ``config`` - A list of integers representing the configuration.

        OUTPUT:

        None

        NOTES:

        Negative amounts of sand are allowed.

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0]])
            >>> srem.setConfig([3,4])
            >>> srem.getConfig()
                [3, 4]
            >>> srem.setConfig([-20, 15])
            >>> srem.getConfig()
                [-20, 15]
        """

        
        self.send("set_config "+self.formatSeq(config))
        self.__checkResult(self.receive())
        self.__tryRepaint()

    def addConfig(self, config):
        r"""
        Adds the given configuration to the current configuration in the program.

        INPUT:

        ``config`` - A list of integers representing the configuration.

        OUTPUT:

        None

        NOTES:

        Negative amounts of sand are allowed.

        EXAMPLES::

            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0]])
            >>> srem.setConfig([3,4])
            >>> srem.getConfig()
                [3, 4]
            >>> srem.adConfig([7, 8])
            >>> srem.getConfig()
                [10, 12]
        """
        self.send("add_config "+self.formatSeq(config))
        self.__checkResult(self.receive())
        self.__tryRepaint()

    def getUnstables(self):
        r"""
        Gets a list of the unstable vertices.

        INPUT:

        None

        OUTPUT:

        A list of ints that are the indices of the unstables vertices.

        NOTES:

        Should never return sinks.

        EXAMPLES::
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0], [10.0, 0]])
            >>> srem.addEdges([[0, 1, 1], [1, 0, 10], [1, 10, 10]])
            >>> srem.getUnstables()
                []
            >>> srem.setConfig([2, 17, 0])
            >>> srem.getUnstables()
                [0]
            >>> srem.addConfig([0, 5, 3])
            >>> srem.getUnstables()
                [0, 1]
        """

        
        self.send("get_unstables")
        return map(int, self.receive().split(","))

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

        Suppose we wish to calculate the number of firings that take
          place on a 20x20 grid while stabilizing the max stable
          plus one grain everywhere.
            
            >>> srem.getToMaxStable()
            >>> len(srem.getConfig())
                480    # Note that the additional 80 are from the sinks
                       # around the edges.
            >>> srem.addConfig([1]*480)    # Add ones everywhere
            >>> numUnstables = srem.getNumUnstables()
            >>> numUnstables
                480    # Note that the sinks never register as unstable.
            >>> total = numUnstables
            >>> while numUnstables > 0:
                    srem.update()
                    numUnstables = srem.getNumUnstables()
                    total += numUnstables
            # At this point, we watch the graph stabilize.
            # If wish to turn off repainting to speed up the stabilization
            # simply turn it off in the visual options tab.
            >>> total
                11556
        """
        self.send("get_num_unstables")
        return int(self.receive())

    def isSink(self, vert):
        r"""
        Tells whether or the indicated vertex is a sink.

        INPUT:

        ``vert`` - The index (an int) of the vertex.

        OUTPUT:

        boolean; True means that the vertex is a sink.

        EXAMPLES::
            >>> srem = SandpileRemote()
            >>> srem.connect()
            >>> srem.addVertices([[0.0, 0.0], [5.0, 5.0], [10.0, 0]])
            >>> srem.addEdges([[0, 1, 1], [1, 0, 10], [1, 10, 10]])
            >>> srem.isSink(0)
                False
            >>> srem.isSink(2)
                True
        """ 
        self.send("is_sink "+str(vert))
        response = self.receive()
        if(response=="true"):
            return True
        else:
            return False

    def getSinks(self):
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
                [2]
            >>> srem.addVertex(-5.0, -5.0)
            >>> srem.getSinks()
                [2, 3]
        """
        self.send("get_sinks")
        return map(int, self.receive().split(","))

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


    def __formatSeq(self, seq):
        return reduce(lambda s, x : s+","+str(x), seq[1:], str(seq[0]))
    
    def __formatSeqOfSeqs(self, seq):
        return reduce(lambda s, x : s+" "+self.__formatSeq(x), seq[1:], self.__formatSeq(seq[0]))

    
