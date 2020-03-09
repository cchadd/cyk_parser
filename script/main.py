import pickle
import argparse
from nltk.tree import Tree
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-s", '--sentences', required=True, help="Path to sentences to parse")
ap.add_argument("-f", '--file_to_store', required=True, help="Path to store the parsed sentences (this will create a file)")
ap.add_argument('-p', '--path_to_parser', required=True, help='Path to parser')

args = vars(ap.parse_args())



if args["path_to_parser"]:
    print('loading parser ... \n')
    
    try:
        with open(args["path_to_parser"], 'rb') as parser:
            cyk = pickle.load(parser)
    
    except FileNotFoundError as e:
        print('Please enter a valid path to parser ! (check -p argument)')
        sys.exit(1)
        
        

try:
    # Collect sentences
    f = open(args['sentences'], 'r')

    test_sentence = []
    for sent in f:
        test_sentence.append(sent.rstrip())
    f.close()

except FileNotFoundError:
        print('Please enter a valid path to sentences ! (check -s argument)')
        sys.exit(1)


try:
    f = open(args['file_to_store'], 'w+')
    for sentence in test_sentence:
        print(sentence)
        (table, dic) = cyk.parse(sentence)
        node = cyk.get_best_tree()
        f.write(cyk.build_tree(node, is_root=True) + "\n")
    f.close()
    print("Done !")
except (NameError, AttributeError, TypeError):
    print('Please enter a valid path to parser ! check (-p argument)')
    sys.exit(1)