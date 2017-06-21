NLP: The Perceptron Algorithm for Dependency Parsing

This repository has an implementation of Dependency Parser, using the Perceptron Algorithm.
You can find more information regarding dependency parsing here:
1. http://www.cs.columbia.edu/~mcollins/6864/slides/glm3.4up.pdf
2. http://faculty.cse.tamu.edu/huangrh/Spring17/l12_Parsing-Dependency_2.pdf

Enjoy!
Roi Sinoff & Orr Krupnik, Jan 2017

***************************************************************************************************
How to run:
Run main.py - the input arguments (mandatory and not-mandatory) are listed in the main file itself.
Example input files can be found at "Data" and "Input_files_examples" directories (see explanation below).

***************************************************************************************************
Directories:

Data:
The data used in this repo is taken from WSJ test-set:
1. *train*.labeled files:
Labeled data used for the learning stage. All of these files are defering (words change of order, less data etc.) from train.labeled
2. test.labeled file:
Labeled data used for infereing. This file is used for checking the results of our learning, and fixing the parameteres, such as which features are used.
2. comp.unlabeled file:
Unlabeled data which was used later in the "test" stage.

Results:
This directory includes results from some of the runs. More details regarding the runs can be found in the excel file in the Results directory.

Input files examples:
Includes example files for feature list input file & files containing examples of run args (loading / learning).

Code:
1. main: 
Calls the data parser, learning, infereing & testing stages, and in the end the comperator (error rate calculator).

2. features: 
Functions for dealing with the features (mainly creating). If you wish to add more features - simply create a lambda & set functions (see examples in file).
All features are kept in dictionaries (or dictionary of dictionaries). 
For example: p_word, c_word, c_pos is saved as a dictionary where the parent words are keys, and each key the value is another dictionary whose key is child words, and values are the child part of speech.
Many of the features we implemented are mentioned in the following article:
Chen, Wenliang, Yue Zhang, and Min Zhang. "Feature Embedding for Dependency Parsing." COLING. 2014.
(link: http://www.aclweb.org/anthology/C14-1078)

3. classes:
Classes for edge (between two words) and sentence (a tree of edges).

4. depparser: 
Parses the input files either for creating the features or for comparing between two files containing labeled sentences.

5. Learning:
Updates the feature weights using Perceptron algorithm which is updated by trying to create the best dependency tree (Maximal Spanning Tree) and comparing it to the real tree.

6. inference:
Inferes the best dependency tree from given sentence and trained weight vector. Has two modes - see more details at in-file comments.

7. edmones: 
An implementation of Chu-Lui/Edmond's algorithm to find MST (minimal spanning tree).
Please note that this code is open source and we found bugs in it (for example, not always creates a tree - sometimes there are circles). 
For original repo see: https://github.com/mlbright/edmonds/blob/master/edmonds/edmonds.py

***************************************************************************************************
Output files:
Creates a new directory with time-stamp, including:
- input files backup
- output files (labeled data - .results files)
- text files for debugging purposes
- numpy array files for loading data without re-learning (just inference/test).