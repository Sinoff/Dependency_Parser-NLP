import os
import sys
import datetime
from parser import corpus_parser
import Learning
import inference


def main(input_args):

    # initializations #
    # create results directory
    subdirectory = "results_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    os.mkdir(subdirectory)
    with open(os.path.join(subdirectory, "cmdline_input.txt"), 'w') as cmdline_file:
        for arg in input_args:
            if arg:  # save command line arguments (only if they exist)
                cmdline_file.write(arg + " ")

    if input_args.m_file:  # advanced model
        with open(input_args.test_file, 'r') as f:
            model_features = [line.split() for line in f.readlines()]

        # todo: compile with Orr's code

    else:  # basic model
        print("basic model selected")
        # todo: compile with Orr's coder

    # training (AKA learning) #
    if input_args.l_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase began: {}".format(parse_time_begin))
        features_num, learning_sentences = corpus_parser(input_args.l_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        # todo: save in log file how many features of each kind were created
        # todo: add save parsed sentences option

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase began: {}".format(run_time_begin))
        weights = Learning.learning_algorithm(input_args.l_iterations, learning_sentences, features_num)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase ended. took {}".format(run_time_end - run_time_begin))

    # todo: decide what to do if we don't have a learning file input (must conclude with having a weights np array)

    # inference (AKA test) #
    if input_args.i_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase began: {}".format(parse_time_begin))
        _, inference_sentences = corpus_parser(input_args.i_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase began: {}".format(run_time_begin))
        for sentence in inference_sentences:
            inference.inference(sentence, weights)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase ended. took {}".format(run_time_end - run_time_begin))

        # todo: output the results of the inference.
        # print the inference results
        with open(os.path.join(subdirectory,"test.results"), 'w') as test_file:
            for sentence in inference_sentences:
                test_file.write(sentence + "\n")

    # comp #
    if input_args.c_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Test parse phase began: {}".format(parse_time_begin))
        _, comp_sentences = corpus_parser(input_args.c_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Test parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Test phase began: {}".format(run_time_begin))
        for sentence in comp_sentences:
            inference.inference(sentence, weights)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Test phase ended. took {}".format(run_time_end - run_time_begin))

        # print the test results
        with open(os.path.join(subdirectory, "comp.labeled"), 'w') as comp_file:
            for sentence in comp_sentences:
                comp_file.write(sentence + "\n")

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
    parser.add_argument('--c_file', type=str, default='', help='name of comp file')

    args = parser.parse_args()

    # Argument Validation #

    if args.m_file and not os.path.exists(args.m_file):
        sys.exit('Model file not found')

    if args.l_file and not os.path.exists(args.l_file):
        sys.exit('Learning file not found')

    if args.i_file and not os.path.exists(args.i_file):
        sys.exit('Inference (AKA test) file not found')

    if args.c_file and not os.path.exists(args.t_file):
        sys.exit('Competition file not found')

    # Run Program #
    main(args)
