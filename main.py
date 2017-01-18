import os
import sys
import datetime
from parser import corpus_parser
import Learning
import inference
import numpy as np


# todo: every print add also to log file?


def main(args):

    # model initializations #

    if args.m_file: #advanced model
        with open(args.test_file, 'r') as f:
            model_features = [line.split() for line in f.readlines()]

        # todo: compile with Orr's code

    else: # basic model
        # todo: compile with Orr's coder

    # training (AKA learning) #
    if args.l_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase began: {}".format(parse_time_begin))
        features_num, learning_sentences = corpus_parser(args.l_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        # todo: save in log file how many features of each kind were created (also time prints?)
        # todo: add save parsed sentences option

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase began: {}".format(run_time_begin))
        weights = Learning.learning_algorithm(args.l_iterations, learning_sentences, features_num)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase ended. took {}".format(run_time_end - run_time_begin))

    # todo: decide what to do if we don't have a learning file input (must conclude with having a weights np array)

    # inference #
    if args.i_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase began: {}".format(parse_time_begin))
        _, inference_sentences = corpus_parser(args.i_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase began: {}".format(run_time_begin))
        for sentence in inference_sentences:
            inference.inference(sentence, weights)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase ended. took {}".format(run_time_end - run_time_begin))

        # todo: output the results of the inference.

    # test #
    if args.t_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Test parse phase began: {}".format(parse_time_begin))
        _, test_sentences = corpus_parser(args.t_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Test parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Test phase began: {}".format(run_time_begin))
        for sentence in test_sentences:
            inference.inference(sentence, weights)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Test phase ended. took {}".format(run_time_end - run_time_begin))

        # todo: output the results of the test.

    # todo: add confusion matrix function call?

    print("done!")


if __name__ == '__main__':

    import argparse as ap

    parser = ap.ArgumentParser()

    # model file - represented as one line of feature numbers, separated by space.
    parser.add_argument('--m_file', type=str, default='',
                        help='name of model file: one line of integers separated by space')

    # learning
    parser.add_argument('--l_file', type=str, default='', help='name of learning file')
    parser.add_argument('--l_iterations', type=int, choices=[20, 50, 80, 100], default=20,
                        help='number of learning iterations')

    # inference
    parser.add_argument('--i_file', type=str, default='', help='name of inference file')

    # test
    parser.add_argument('--t_file', type=str, default='', help='name of test file')

    # parser.add_argument('--save', type=str, default='',
    #                     help='Place a name after this to save Corpus and Feature '
    #                          'table output files, with this name')

    args = parser.parse_args()

    # Argument Validation #

    if args.m_file and not os.path.exists(args.m_file):
        sys.exit('Model file not found')

    if args.l_file and not os.path.exists(args.l_file):
        sys.exit('Learning file not found')

    if args.i_file and not os.path.exists(args.i_file):
        sys.exit('Inference file not found')

    if args.t_file and not os.path.exists(args.t_file):
        sys.exit('Test file not found')

    # Run Program #
    main(args)
