import dill
import networkx as nx
from itertools import product

from solver.solve import find_paths, filter_found_paths

def make_graph(grid_shape):
    nodes = [(x, y) for x, y in product(range(grid_shape), range(grid_shape))]
    edges = {}

    for (x, y) in nodes:
        x_edges = [(x, i) for i in range(grid_shape) if i != x]
        y_edges = [(i, y) for i in range(grid_shape) if i != y]
        edges[(x, y)] = x_edges + y_edges

    g = nx.Graph()
    g.add_nodes_from(nodes)

    for node, e_l in edges.items():
        g.add_edges_from([(node, e) for e in e_l])

    return g

if __name__ == '__main__':

    buffer_sizes = [4,5,6,7,8]

    for b in buffer_sizes:
        print(f'Doing grid_shape 5 with buffer_size {b}...')

        graph = make_graph(5)

        data = []

        for start_point in ((0, x) for x in range(5)):
            print(f"\tDoing {start_point}...")

            possible_paths = find_paths(graph, start_point, b-1)

            possible_paths = filter_found_paths(possible_paths)

            data.extend(possible_paths)

        with open(f'data/{b}.dill', 'wb') as fp:
            dill.dump(data, fp)


