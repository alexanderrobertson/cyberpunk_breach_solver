import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

from .solve import solve

class Puzzle:
    def __init__(self, grid_string, targets, valid_chars=('1C', 'E9', 'BD', '55'), buffer_size=4):
        self.characters = valid_chars
        self.char_map = {c[0].lower(): c for c in self.characters}

        self.buffer_size = buffer_size

        self.grid_string = [self.char_map[c] for c in self.validate_string(grid_string)]

        self.grid_shape = int(np.sqrt(len(self.grid_string)))
        self.grid_as_array = self.string_to_array(self.grid_string)

        self.targets = [[self.char_map[c] for c in t] for t in self.validate_targets(targets).split()]

        self.graph = self.make_graph()

        self.solution = solve(self)

    def validate_string(self, s, shape=True):
        if shape:
            shape_check = np.sqrt(len(s)).is_integer()
            if not shape_check:
                raise ValueError(f"String has {len(s)} items, which is not square")

        char_check = set(s).difference(self.char_map)
        if char_check:
            raise ValueError(f"Invalid characters: {', '.join(char_check)}. Permitted: {', '.join(self.char_map)}")

        return s

    def validate_targets(self, tl):
        for t in tl.split():
            _ = self.validate_string(t, shape=False)
        return tl

    def string_to_array(self, gs):
        grid = np.reshape(gs, (self.grid_shape, self.grid_shape))
        return grid

    def make_graph(self):
        nodes = [(x, y) for x, y in product(range(self.grid_shape), range(self.grid_shape))]

        edges = {}

        for (x, y) in nodes:
            x_edges = [(x, i) for i in range(self.grid_shape) if i != x]
            y_edges = [(i, y) for i in range(self.grid_shape) if i != y]

            edges[(x, y)] = x_edges + y_edges

        g = nx.Graph()
        g.add_nodes_from(nodes)

        node_labels = {n: self.grid_as_array[n] for n in g.nodes}

        nx.set_node_attributes(g, node_labels, 'label')

        for node, e_l in edges.items():
            g.add_edges_from([(node, e) for e in e_l])

        return g

    def plot_graph(self, display=True):
        fig, ax = plt.subplots(ncols=2, figsize=(16, 8))

        node_labels = nx.get_node_attributes(self.graph, 'label')

        coords = [[[r, c] for c, v2 in enumerate(v1)] for r, v1 in enumerate(self.grid_as_array)]

        coords = np.rot90(coords).reshape(-1, 2)

        pos1 = {n: p for n, p in zip(self.graph.nodes(), coords)}

        nx.draw(self.graph, pos1, ax=ax[0])
        nx.draw_networkx_labels(self.graph, pos1, labels=node_labels, ax=ax[0])

        pos2 = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos2, labels=node_labels, ax=ax[1])

        if display:
            plt.show()

        return fig

    def plot_solultion(self, display=True):
        pass

    def __repr__(self):
        g = '\n\t'.join([' '.join(v for v in r) for r in self.grid_as_array])
        t = '\n\t'.join([' '.join(v for v in r) for r in self.targets])
        if self.solution:
            sp = self.solution["path"][0][1]+1
            fp = self.solution["path"]
            seq = self.solution["sequence"]
            hp = [f"{p}:{x+1}-{y+1}" for p, (x,y) in zip(seq, self.solution["path"])]
            m = self.solution["matched"]
            s = f'\tStart at item {sp} in top row\n\tFull path:{fp}\n\tHuman path:{hp}\n\tSequence:{seq}\n\tMatched:{m}'
        else:
            s = '\tNo solution possible.'
        return f"Grid with shape {self.grid_shape}x{self.grid_shape}:\n\t{g}\nTargets:\n\t{t}\nSolution:\n{s}"




















