class EdgeData(object):
    """ EdgeData class holds all data relating to an edge, to enable easy
        feature extraction. 
    """
    def __init__(self, sentence, p_ind, c_ind):
        self.p_ind = p_ind
        self.c_ind = c_ind
        self.p_word = sentence.words[p_ind]
        self.p_pos = sentence.pos[p_ind]
        self.c_word = sentence.words[c_ind]
        self.c_pos = sentence.pos[c_ind]
        self.dist = c_ind - p_ind
        self.sen_len = len(sentence.words) - 1

        # Parent previous POS
        if p_ind > 1:
            self.p_pre_pos = sentence.pos[p_ind-1]
        else:
            self.p_pre_pos = None

        # Parent next POS
        if p_ind < self.sen_len - 1 and p_ind != 0:  
            self.p_next_pos = sentence.pos[p_ind + 1]
        else:
            self.p_next_pos = None
        
        # Child previous POS
        if c_ind > 1:
            self.c_pre_pos = sentence.pos[c_ind-1]
        else:
            self.c_pre_pos = None
            
        # Child next POS
        if c_ind < self.sen_len - 1 and c_ind != 0:  
            self.c_next_pos = sentence.pos[c_ind + 1]
        else:
            self.c_next_pos = None
        

class Sentence(object):
    """ Sentence class - holds all data relating to parsed sentence
    """
    def __init__(self, sen_block, training):
        """ Parse an input sentence block into the Sentence class
        """
        # parse sentence block from input file into data structure
        lines = [line.split('\t') for line in sen_block.split('\n') 
                 if line != '']
        properties = zip(*lines)
        # Add root word
        self.words = ['ROOT'] + list(properties[1])
        self.pos = ['ROOT'] + list(properties[3])
        self.edges = []
        self.edge_data = {}
        # Makes it easier to recreate file when printing
        self.heads = ['_']*len(self.words)
        self.dependencies = ['_']*len(self.words)
        # The training flag enables not parsing correct edges from test file
        if training:
            for c, p in enumerate(properties[6], 1):
                self.add_edge(int(p), c)
                self.dependencies[c] = properties[7][c - 1]
        # This holds all indeices of features active in the sentence, and how
        # many times they appear
        self.feat_inds = {}

    def add_edge(self, p_ind, c_ind):
        """ Add an edge in all its representation forms (including data)
        """
        self.heads[c_ind] = p_ind
        self.edges.append((p_ind, c_ind))
        if p_ind in self.edge_data:
            self.edge_data[p_ind][c_ind] = EdgeData(self, p_ind, c_ind)
        else:
            self.edge_data[p_ind] = {c_ind : EdgeData(self, p_ind, c_ind)}

    def __repr__(self):
        """ Print sentence in the shape of a sentence block (good for creating
            output file)
        """
        emptys = ['_']*len(self.words[1:])
        data = zip(range(1, len(self.words) + 1), self.words[1:], emptys, 
                   self.pos[1:], emptys, emptys, self.heads[1:], emptys,
                   emptys, emptys)
        text = '\n'.join(['\t'.join([str(obj) for obj in 
                          line]) for line in data])
        return text

    def __str__(self):
        # Easy debug representation of sentence
        return ' '.join([word + '_' + pos for word, pos in 
                         zip(self.words, self.pos)[1:]]) + '\n'