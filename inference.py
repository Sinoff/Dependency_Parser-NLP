from features import get_feature_list
from edmonds import mst


def tree_score(tree):
    score = 0    
    for parent in tree.keys():
        for child in tree[parent].keys():
            score += tree[parent][child]
    return score


def inference(sentence, weights):
    best_tree = {}
    for w, word in enumerate(sentence.words[1:], 1):        
        weights_graph = {}
        # find best tree
        for p, parent in enumerate(sentence.words[1:], 1):
            weights_graph[p] = {}
            for c, child in enumerate(sentence.words[1:], 1):
                if p != c:  # cannot have self edges
                    weights_graph[p][c] = -sum(weights[get_feature_list(sentence, p, c)])
        
        # add root node
        weights_graph[0] = {w : -sum(weights[get_feature_list(sentence, w, c)])}
    
        # call Edmonds - 0 is root    
        weights_tree = mst(0, weights_graph)
        if w == 1:
            best_tree = weights_tree
        else: 
            if tree_score(best_tree) > tree_score(weights_tree):
                best_tree = weights_tree
 
    for parent in best_tree.keys():
        for child in best_tree[parent].keys():
            sentence.add_edge(parent, child)
            