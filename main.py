import os
import sys
import datetime
from depparser import parse
import Learning
import inference
import numpy as np
import features


def main(input_args):

    # initializations #
    # create results directory
    subdirectory = "results_" + datetime.datetime.now().strftime("%d_%m-%H%M%S")
    os.mkdir(subdirectory)
    with open(os.path.join(subdirectory, "cmdline_input.txt"), 'w') as cmdline_file:
        for arg in vars(input_args):
            if getattr(input_args, arg):
                cmdline_file.write("{}={} ".format(arg, getattr(input_args, arg)))

    if input_args.m_file:  # advanced model
        with open(input_args.test_file, 'r') as f:
            model_features = [line.split() for line in f.readlines()]

        # todo: compile with Orr's code

    else:  # basic model
        print("basic model selected")
        # todo: compile with Orr's coder

    # training (AKA learning) #
    if input_args.learn:  # learn new weights and features
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase began: {}".format(parse_time_begin))
        features_num, learning_sentences = parse(input_args.l_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        #  save in log file how many features of each kind were created
        feature_amounts = features.get_amounts()
        with open(os.path.join(subdirectory, "featureNums.txt"), 'w') as featureAmountFile:
            for amount in feature_amounts:
                featureAmountFile.write(amount.key + ": " + amount.value + "\n")
        # save features as pickle
        features.save_features(subdirectory)

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase began: {}".format(run_time_begin))
        weights = Learning.learning_algorithm(input_args.l_iterations, learning_sentences, features_num)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase ended. took {}".format(run_time_end - run_time_begin))
        np.save(os.path.join(subdirectory, "weights"), weights)

    else:  # loading previous learn inputs
        weights = np.load(os.path.join(input_args.l_file, "weights"))
        features.load_features(input_args.l_file)

    # inference (AKA test) #
    if input_args.i_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase began: {}".format(parse_time_begin))
        _, inference_sentences = parse(input_args.i_file)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase began: {}".format(run_time_begin))
        for sentence in inference_sentences:
            inference.inference(sentence, weights)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase ended. took {}".format(run_time_end - run_time_begin))

        # print the inference results
        with open(os.path.join(subdirectory, "test.results"), 'w') as test_file:
            for sentence in inference_sentences:
                test_file.write(sentence + "\n")

    # comp #
    if input_args.c_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Test parse phase began: {}".format(parse_time_begin))
        _, comp_sentences = parse(input_args.c_file)
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
    parser.add_argument('--learn', type=bool, default=True, help='bool flag: learning (= True) or loading (= False)')
    parser.add_argument('l_file', type=str, default='',
                        help='name of learning file. If learn == True, it is the path to train.labeled,'
                        'else - it is a **dir** path to where all loading files are')

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
