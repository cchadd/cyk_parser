import re
import nltk
from sklearn.model_selection import train_test_split
from nltk.tree import Tree
from nltk import Nonterminal, induce_pcfg, treetransforms



class CPFG_CNF(object):


    @classmethod
    def get_trees(cls, path_to_dataset, train_split=0.8):
        """
        This methods returns the train, test and eval set as list of trees

        Inputs:
        -------

        path_to_dataset (str): The path to the copus to be split
        train_split (float): Proportion of training
        """
        sentences = []
        print('Collecting training, test and evaluation trees')
        with open(path_to_dataset) as f:

            for sentence in f:
                # Removes functional labels
                sent = re.sub(r'-\w+\ ', " ", sentence)
                sentences.append(sent.rstrip())

        # Split Train / (Test + Eval)
        train_sent, test_sent = train_test_split(sentences, train_size=train_split, test_size=1 - train_split, shuffle=False)

        # Split Test / Eval
        eval_sent, test_sent = train_test_split(test_sent, train_size=0.5, shuffle=False)

        print(f'The total number of sentences {len(sentences)}')
        print(f'Number of train sentences {len(train_sent)} -- {round(100 * len(train_sent)  / len(sentences), 1)} %')
        print(f'Number of test sentences {len(test_sent)} -- {round(100 * len(test_sent)  / len(sentences), 1) } %')
        print(f'Number of evaluation sentences {len(eval_sent)} -- {round(100 * len(eval_sent)  / len(sentences), 1)} %')


        train_trees = [Tree.fromstring(sent, remove_empty_top_bracketing=True) for sent in train_sent]
        test_trees  = [Tree.fromstring(sent, remove_empty_top_bracketing=True) for sent in test_sent]
        eval_trees = [Tree.fromstring(sent, remove_empty_top_bracketing=True) for sent in eval_sent]

        for (test, ev) in zip(test_trees, eval_trees):

            # Remove unary rules
            treetransforms.collapse_unary(test)
            treetransforms.collapse_unary(ev)

            # Transform to CNF
            treetransforms.chomsky_normal_form(test, horzMarkov=2)
            treetransforms.chomsky_normal_form(ev, horzMarkov=2)


        return train_trees, eval_trees, test_trees



    @classmethod
    def get_grammar(cls, train_trees, starting_symb='SENT'):
        """
        This method returns a the grammar coputed from the training set.

        Inputs:
        -------

        train_trees (list): List of trees to perform training
        startting_symbol (str): The root symbol
        """
        productions = []

        # Chmosky Normal Form
        for tree in train_trees:
            
            # Remove unary rules
            treetransforms.collapse_unary(tree)

            # Transform to CNF
            treetransforms.chomsky_normal_form(tree, horzMarkov=2)

            # Copute production and store is
            productions += tree.productions()

        # Define the root symbol
        SENT = Nonterminal(starting_symb)

        # Compute the grammar using PCFG
        grammar = induce_pcfg(SENT, productions)

        grammar.chomsky_normal_form()

        return grammar

    @classmethod
    def decode_tree(cls, tree):

        """
        Decode the input tree and outputs the corresponding sentence
        """

        return ' '.join(tree.leaves())


    @classmethod
    def get_lexicon(cls, train_trees):
        """
        Derives the lexicon i.e. the terminal words over the corpus
        """
        lexicon = [word for tree in train_trees for word in CPFG_CNF.decode_tree(tree).split(' ')]

        return list(dict.fromkeys(lexicon))