# -*- coding: utf-8 -*-

from classes import Sentence
import features


def parse(filename, training):
    with open(filename, 'r') as f:
        sen_blocks = f.read().split('\n\n')
        if not len(sen_blocks[-1]):
            del sen_blocks[-1]
        
    sentences = []
    for block in sen_blocks:
        # First, create sentence
        sentence = Sentence(block, training)
        # Then, create all relevant features        
        if training:
            for p, c in sentence.edges:
                f_inds = features.set_features(sentence.edge_data[p][c])
                for f in f_inds:
                    if f in sentence.feat_inds:
                        sentence.feat_inds[f] += 1
                    else:
                        sentence.feat_inds[f] = 1
                        
        sentences.append(sentence)
        
    return sentences


def parse_for_comparison(file1, file2):
    """ Parse two files and compare head tokens. 
        Implements multiple error counters to figure out where 
        most parsing errors lie, in terms of dependency labels.
    """
    sen_blocks = [[], []]    
    for ind, filename in enumerate([file1, file2]):
        with open(filename, 'r') as f:
            sen_blocks[ind] = f.read().split('\n\n')
            if not len(sen_blocks[ind][-1]):
                del sen_blocks[ind][-1]
        
    total_edges = 0
    wrong_edges = 0
    wrong_edge_types = {}
    all_edge_types = {}
    golden_sens = []

    for block1, block2 in zip(*sen_blocks):
        sentence1 = Sentence(block1, True)
        sentence2 = Sentence(block2, True)
        assert((sentence1.words == sentence2.words) and 
               (sentence1.pos == sentence2.pos)), "Files compared have different sentences"
        
        for w, dep, h1, h2 in zip(sentence1.words, sentence1.dependencies, 
                               sentence1.heads, sentence2.heads):
            total_edges += 1
            if dep in all_edge_types:
                all_edge_types[dep] += 1
            else:
                all_edge_types[dep] = 1
            
            if h1 != h2:
                # Wrong head --> wrong edge
                wrong_edges += 1
                                    
                if dep in wrong_edge_types:
                    wrong_edge_types[dep] += 1
                else:
                    wrong_edge_types[dep] = 1
        
        sentence1.dependencies = ['_']*len(sentence1.words)
        golden_sens.append(sentence1)
        
    print("Histogram of wrong dependency percentages | "
          "Percentage out of all dependency types: \n")    
    for dep_type in wrong_edge_types:
        print("{}: {} | {}".format(dep_type, 
              100.0 * wrong_edge_types[dep_type] / wrong_edges, 
              100.0 * all_edge_types[dep_type] / total_edges))
    
    return 100.0 * wrong_edges / total_edges, golden_sens