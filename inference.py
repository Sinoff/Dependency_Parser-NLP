from features import get_feature_list
from edmonds import mst


def tree_score(tree):
    score = 0    
    for parent in tree.keys():
        for child in tree[parent].keys():
            score += tree[parent][child]
    return score


def inference(sentence, weights, one_tree):
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

        # Enables using the vanilla algorithm with all edges from root
        if one_tree:     
            for c, child in enumerate(sentence.words[2:], 2):
                weights_graph[0][c] = -sum(weights[get_feature_list(sentence, 0, c)])
            
        # call Edmonds - 0 is root    
        weights_tree = mst(0, weights_graph)
        if w == 1:
            best_tree = weights_tree
        else: 
            if tree_score(best_tree) < tree_score(weights_tree):
                best_tree = weights_tree
        
        if one_tree:
            break
        
    for parent in best_tree.keys():
        for child in best_tree[parent].keys():
            sentence.add_edge(parent, child)

    # child_list = [c for p, c in sentence.edges]
    # assert set(child_list) == set(range(1, len(sentence.words))), "Child list does not include all: \n{},\n{}".format(sorted(child_list), repr(sentence))
    # assert len(set(child_list)) == len(child_list), "Child list is not unique: \n{},\n{}".format(sorted(child_list), repr(sentence))
    # assert 0 not in child_list, "ROOT in child list! \n{}".format(repr(sentence))
    # assert 0 in [p for p, c in sentence.edges], "ROOT not a parent: \n{}".format(repr(sentence))
            