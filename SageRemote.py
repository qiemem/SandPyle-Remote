from SandpileRemote import *

class SageRemote:

    def __init__(self):
        self.srem = SandpileRemote()
        self.labels_to_indices = dict()
        self.indices_to_labels = list()

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

    def delete_graph(self):
        r"""
        Tells the program to delete all vertices and edges.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.delete_graph()
        """
        self.srem.delete_graph()
        self.labels_to_indices = dict()
        self.indices_to_labels = list()

    def clear_sand(self):
        r"""
        Sets each vertex to 0 grains of sand.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.clear_sand()
        """
        self.srem.clear_sand()

    def get_graph(self, sink_label = 'sink'):
        r"""
        Retrieves the current graph in the program.

        INPUT:

        None

        OUTPUT:

        A DiGraph.

        EXAMPLES::
        
        """
        self.sink_label = sink_label
        self.indices_to_labels = list()
        self.labels_to_indices = dict()
        vertex_pos_list = self.srem.get_vertices()
        sinks = set(self.srem.get_sinks())
        edges = self.srem.get_edges()
        vertex_pos_dict = dict()
        graph_data={self.sink_label : {}}
        for v in range(len(vertex_pos_list)):
            if v in sinks:
                self.indices_to_labels.append(self.sink_label)
            else:
                self.indices_to_labels.append(v)
                self.labels_to_indices[v]=v
                graph_data[v] = dict()
                vertex_pos_dict[v]=vertex_pos_list[v]
        for e in edges:
            if e[1] in sinks:
                graph_data[e[0]][self.sink_label] = e[2]
            else:
                graph_data[e[0]][e[1]]=e[2]
        return DiGraph(data=graph_data, pos=vertex_pos_dict)

    def set_graph(self, graph, sink_label = 'sink', scale=10.0, offset = (0.0, 0.0)):
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
        self.sink_label = sink_label
        pos_dict = graph.get_pos()
        if pos_dict is None:
            sinkless_graph = deepcopy(graph)
            sinkless_graph.delete_vertex(sink_label)
            sinkless_graph.plot(save_pos=True)
            pos_dict = sinkless_graph.get_pos()
            pos_dict[sink_label]=offset
        self.labels_to_indices = dict()
        self.indices_to_labels = list()
        vertex_positions = list()
        for v in graph.vertices():
            self.labels_to_indices[v] = len(self.indices_to_labels)
            self.indices_to_labels.append(v)
            pos = pos_dict[v]
            vertex_positions.append([scale * pos[0] + offset[0], scale*pos[1] + offset[1]])
        self.srem.delete_graph()
        self.srem.add_vertices(vertex_positions)
        edges = list()
        for e in graph.edges():
            if e[0]!=self.sink_label:
                edges.append([self.labels_to_indices[e[0]], self.labels_to_indices[e[1]], e[2]])
        self.srem.add_edges(edges)
            

    def get_config(self):
        config = self.srem.get_config()
        labelled_config = {}
        for i in range(len(config)):
            labelled_config[self.indices_to_labels[i]] = config[i]
        return labelled_config

    def get_sand(self, vert):
        return self.srem.get_sand(self.labels_to_indices[vert])

    def set_sand(self, vert, amount):
        self.srem.set_sand(labels_to_indices[vert], amount)

    def add_sand(self, vert, amount):
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
        self.srem.add_sand(labels_to_indices[vert])

    def add_random_sand(self, amount):
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
        self.srem.add_random_sand(amount)
        
    def set_config(self, config):
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
        self.srem.set_config(self.__labelled_config_to_indexed(config))

    def add_config(self, config):
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
        self.srem.add_config(self.__labelled_config_to_indexed(config))

    def get_unstables(self):
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
        return self.__indexed_vertices_to_labelled(self.srem.get_unstables())

    def get_num_unstables(self):
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
        return self.__indexed_vertices_to_labelled(self.srem.get_unstables())

    def is_sink(self, vert):
        r"""
        Tells whether or the indicated vertex is a sink.

        INPUT:

        ``vert`` - The label of the vertex.

        OUTPUT:

        boolean; True means that the vertex is a sink.

        EXAMPLES::
        """ 
        return self.srem.is_sink(self.labels_to_indices[vert])

    def get_sinks(self):
        r"""
        Returns a list of all the sinks.

        INPUT:

        None
      
        OUTPUT:
        
        A list of the labels of the sinks.

        EXAMPLES::
        """
        return self.__indexed_vertices_to_labelled(self.srem.get_sinks())

    def get_nonsinks(self):
        r"""
        Returns a list of all the sinks.

        INPUT:

        None
      
        OUTPUT:
        
        A list of the labels of the sinks.

        EXAMPLES::
        """
        return self.__indexed_vertices_to_labelled(self.srem.get_sinks())

    def get_selected(self):
        r"""
        Returns a list of all the vertices that are currently
          selected in the program.

        INPUT:

        None

        OUTPUT:

        A list of the labels of the selected vertices.

        EXAMPLES::
        """
        return self.__indexed_vertices_to_labelled(self.srem.get_selected())

    def get_config_named(self, name):
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

        return self.__indexed_config_to_labelled(self.srem.get_config_named(name))
    
    def set_to_max_stable(self):
        r"""
        Sets the current configuration to the max stable configuration.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.set_to_max_stable()
        """

        self.srem.set_to_max_stable()

    def add_max_stable(self):
        self.srem.add_max_stable()

    def get_max_stable(self):
        return self.__indexed_config_to_labelled(self.srem.get_max_stable())

    def set_to_identity(self):
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

            >>> srem.set_to_identity()
        """
        self.srem.set_to_identity()

    def add_identity(self):
        r"""
        Adds the identity configuration to the current configuration_x_s.

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

            >>> srem.add_identity()
        """
        self.srem.add_identity()

    def get_identity(self):
        return self.__indexed_config_to_labelled(self.srem.get_identity())

    def set_to_burning(self):
        r"""
        Sets the current configuration to the minimal burning
          configuration.

        INPUT:

        None

        OUTPUT:

        None

        EXAMPLES::

            >>> srem.set_to_burning()
        """
        self.srem.set_to_burning()

    def add_burning(self):
        self.srem.add_burning()

    def get_burning(self):
        return self.__indexed_config_to_labelled(self.srem.get_burning())

    def set_to_dual(self):
        self.srem.set_to_dual()

    def add_dual(self):
        self.srem.add_dual()

    def get_dual(self):
        return self.__indexed_config_to_labelled(self.srem.get_dual())


    def __labelled_config_to_indexed(self, config):
        new_config = [0]*len(self.indices_to_labels)
        for v in config:
            if v != self.sink_label:
                new_config[self.labels_to_indices[v]]=config[v]
        return new_config

    def __indexed_config_to_labelled(self, config):
        new_config  = dict()
        for v in config:
            if self.indices_to_labels[v]!=self.sink_label:
                new_config[self.indices_to_labels[v]] = config[v]
        return new_config

    def __labelled_vertices_to_indexed(self, vertices):
        return map(lambda v : self.labels_to_indices[v], vertices)
    
    def __indexed_vertices_to_labelled(self, vertices):
        return filter( lambda v : v!=self.sink_label, map(lambda v : self.indices_to_labels[v], vertices))

    
