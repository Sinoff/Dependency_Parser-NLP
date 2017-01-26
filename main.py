import os
import sys
import datetime
import depparser as dpp
import Learning
import inference
import numpy as np
from shutil import copyfile


def main(input_args):

    # initializations #
    # create results directory
    subdirectory = "results_" + datetime.datetime.now().strftime("%d_%m-%H%M%S")
    os.mkdir(subdirectory)
    with open(os.path.join(subdirectory, "cmdline_input.txt"), 'w') as cmdline_file:
        for arg in vars(input_args):
            if getattr(input_args, arg):
                cmdline_file.write("{}={} ".format(arg, getattr(input_args, arg)))

    # Model selection (file should include list of features)
    if input_args.m_file:
        dpp.features.set_model_features(input_args.m_file)
        copyfile(input_args.m_file, os.path.join(subdirectory, "features_input.txt"))
    else:
        print("Using all {} feature types.".format(str(dpp.features.num_feat_types)))
        
    # training (AKA learning) #
    if input_args.learn == "True":  # learn new weights and features
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase began: {}".format(parse_time_begin))
        learning_sentences = dpp.parse(input_args.l_file, True)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        #  save in log file how many features of each kind were created
        with open(os.path.join(subdirectory, "feature_amounts.txt"), 'w') as featureAmountFile:
            total = 0
            for feature, value in dpp.features.feat_amounts.items():
                if value != 0:
                    featureAmountFile.write("{} : {}\n".format(feature, value))
                    total += value
            assert (total == dpp.features.num_features), "total amount of features doesn't match sum"
            featureAmountFile.write("total : {}\n".format(dpp.features.num_features))
        # save features as pickle
        dpp.features.save_features(subdirectory)
        # start learning
        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase began: {}".format(run_time_begin))
        weights = Learning.learning_algorithm(input_args.l_iterations, learning_sentences, dpp.features.num_features, subdirectory)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Train phase ended. took {}".format(run_time_end - run_time_begin))

    else:  # loading previous learn inputs
        weights = np.load("{}/weights{}.npy".format(input_args.l_file, input_args.l_iterations))
        dpp.features.features = dpp.features.pickle.load(open("{}/features.dmp".format(input_args.l_file), 'rb'))

    # inference (AKA test) #
    if input_args.i_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase began: {}".format(parse_time_begin))
        inference_sentences = dpp.parse(input_args.i_file, False)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase began: {}".format(run_time_begin))
        for sentence in inference_sentences:
            inference.inference(sentence, weights, args.onetree)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Inference phase ended. took {}".format(run_time_end - run_time_begin))

        # print the inference results
        with open(os.path.join(subdirectory, "test.results"), 'w') as test_file:
            test_file.write('\n\n'.join([repr(s) for s in inference_sentences]))            
  
    # comp #
    if input_args.c_file:
        parse_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Test parse phase began: {}".format(parse_time_begin))
        comp_sentences = dpp.parse(input_args.c_file, False)
        parse_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Test parse phase ended. took {}".format(parse_time_end - parse_time_begin))

        run_time_begin = datetime.datetime.now().replace(microsecond=0)
        print ("Test phase began: {}".format(run_time_begin))
        for sentence in comp_sentences:
            inference.inference(sentence, weights, args.onetree)
        run_time_end = datetime.datetime.now().replace(microsecond=0)
        print ("Test phase ended. took {}".format(run_time_end - run_time_begin))

        # print the test results
        with open(os.path.join(subdirectory, "comp.labeled"), 'w') as comp_file:
            comp_file.write('\n\n'.join([repr(s) for s in comp_sentences]))

    if input_args.i_file:
        perc, comp_sens = dpp.parse_for_comparison(input_args.i_file, subdirectory + "/test.results")
        print("Error percentage: {}".format(perc))
        with open(os.path.join(subdirectory, "test.unlabeled"), 'w') as test_file:
            test_file.write('\n\n'.join([repr(s) for s in comp_sens]))
    print("done!")


if __name__ == '__main__':

    import argparse as ap

    parser = ap.ArgumentParser()

    # model file - represented as one line of feature numbers, separated by space.
    parser.add_argument('--m_file', type=str, default='',
                        help='name of model file: one line of integers separated by space')

    # learning
    parser.add_argument('--learn', type=str, default="True", help='bool flag: learning (= True) or loading (= False)')
    parser.add_argument('l_file', type=str, default='',
                        help='name of learning file. If learn == True, it is the path to train.labeled,'
                        'else - it is a **dir** path to where all loading files are')

    parser.add_argument('--l_iterations', type=int, choices=[20, 50, 80, 100], default=20,
                        help='number of learning iterations')

    # inference
    parser.add_argument('--i_file', type=str, default='', help='name of inference file')

    # test
    parser.add_argument('--c_file', type=str, default='', help='name of comp file')

    parser.add_argument('--onetree', '-o', action='store_true', help='Set this' 
                        ' flag to use one full graph instead of choosing the best of many')
    
    
    args = parser.parse_args()

    # Argument Validation #

    if args.m_file and not os.path.exists(args.m_file):
        sys.exit('Model file not found')

    if args.l_file and not os.path.exists(args.l_file):
        sys.exit('Learning file not found')

    if args.i_file and not os.path.exists(args.i_file):
        sys.exit('Inference (AKA test) file not found')

    if args.c_file and not os.path.exists(args.c_file):
        sys.exit('Competition file not found')

    # Run Program #
    main(args)
