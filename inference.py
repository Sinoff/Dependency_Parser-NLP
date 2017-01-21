from features import get_feature_list
from edmonds import mst


def inference(sentence, weights):
    weights_graph = {}
    # find best tree
    for p, parent in enumerate(sentence.words):
        weights_graph[p] = {}
        for c, child in enumerate(sentence.words[1:], 1):
            if p != c:  # cannot have self edges
                weights_graph[p][c] = -sum(weights[get_feature_list(sentence, p, c)])


    # call Edmonds - 0 is root    
    weights_tree = mst(0, weights_graph)
    for parent in weights_tree.keys():
        for child in weights_tree[parent].keys():
            sentence.add_edge(parent, child)