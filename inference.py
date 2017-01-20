from features import get_feature_list
from edmonds import mst


def inference(sentence, weights):
    weights_graph = {}
    # find best tree
    for p, parent in enumerate(sentence.words)[1:]:
        weights_graph[p] = {}
        for c, child in enumerate(sentence.words[1:], 1):
            if p != c:  # cannot have self edges
                weights_graph[p][c] = sum(weights[get_feature_list(sentence, p, c)])
                weights_graph[p] = {}

    # add root to all others
    for c, child in enumerate(sentence.words[1:], 1):
        weights_graph[0][c] = 0

    # call Edmonds - 0 is root
    mst(0, weights_graph)
    for p, parent in enumerate(weights_graph):
        for c, child in enumerate(weights_graph[p]):
            sentence.add_edge(p, c)
