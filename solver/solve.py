import dill


def find_paths(G, node, length):
    '''
    Taken from: https://stackoverflow.com/questions/28095646/finding-all-paths-walks-of-given-length-in-a-networkx-graph/28103735#28103735
    '''
    if length == 0:
        return [[node]]

    paths = [[node] + path for neighbor in G.neighbors(node) for path in find_paths(G, neighbor, length - 1) if node not in path]

    return paths

def evaluate_path(path):
    for e, ((x1, y1), (x2, y2)) in enumerate(zip(path, path[1:]), 1):
        if e == 1:
            if x1 != x2:
                continue
            else:
                return False
        if e % 2 == 0:
            if x1 != x2:
                return False
            if y1 == y2:
                return False
        else:
            if x1 == x2:
                return False
            if y1 != y2:
                return False
    return True

def filter_found_paths(paths):
    return [i for i in paths if evaluate_path(i)]

def path_to_sequence(g, path):
    return [g.nodes[n]['label'] for n in path]

def check_solution(graph, target_paths, path):
    target_paths_copy = [i for i in target_paths]

    path = path_to_sequence(graph, path)

    for point in path:
        for e, t in enumerate(target_paths_copy):
            if t:
                if t[0] == point:
                    target_paths_copy[e] = t[1:]

    return [False if len(t) else True for t in target_paths_copy]

def score_solutions(graph, target_paths, solutions):
    best = dict(path=None, score=0)

    for p in solutions:
        matches = check_solution(graph, target_paths, p)
        score = sum([m * w for m, w in zip(matches, [1, 2, 3])])

        if score == 6:
            best['path'] = p
            best['score'] = score
            best['sequence'] = path_to_sequence(graph, p)
            best['matched'] = [e for e, m in enumerate(matches, 1) if m]
            break

        if score > best['score']:
            best['path'] = p
            best['score'] = score
            best['sequence'] = path_to_sequence(graph, p)
            best['matched'] = [e for e, m in enumerate(matches, 1) if m]

    if best['path']:
        return best
    else:
        return None

def solve(puzzle):

    if puzzle.grid_shape == 5:

        with open(f'data/{puzzle.buffer_size}.dill', 'rb') as fp:
            all_paths = dill.load(fp)
        all_paths = filter_found_paths(all_paths)

    else:
        all_paths = []

        start_points = [(0, x) for x in range(puzzle.grid_shape)]

        for start_point in start_points:
            paths = find_paths(puzzle.graph,
                               start_point,
                               puzzle.buffer_size - 1)

            all_paths.extend(filter_found_paths(paths))

    return score_solutions(puzzle.graph, puzzle.targets, all_paths)
















