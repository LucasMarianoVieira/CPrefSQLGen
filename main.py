import gen
import experiment

'''
CPrefSQLGen:
Dataset Generator with Simple Preferences for CprefSQL
'''

def get_arguments(print_help=False):
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('CPrefSQLGen')
    parser.add_argument('-g', '--gen', action="store_true",
                        default=False,
                        help='Generate files')
    parser.add_argument('-o', '--output', action="store_true",
                        default=False,
                        help='Generate query output')
    parser.add_argument('-r', '--run', action="store_true",
                        default=False,
                        help='Run experiments')
    parser.add_argument('-s', '--summarize', action="store_true",
                        default=False,
                        help='Summarize results')
    args = parser.parse_args()
    if print_help:
        parser.print_help()
    return args

def main():
    '''
    Main routine
    '''
    args = get_arguments()
    exp_list = gen_experiment_list(BESTSEQ_CONF)
    if args.gen:
        # generating data
        print('Generating data')
        #gen_all
        print('Generating queries')
        #gen queries
    elif args.run:
        print('Running experiments')
        #run_experiments
    elif args.summarize:
        print('Summarizing results')
        #summarize_all
        #print('Calculating confidence intervals')
        #confidence_interval_all
    else:
        get_arguments(True)


if __name__ == '__main__':
    main()