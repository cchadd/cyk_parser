#%%
import re
import pickle
from cpfg import CPFG_CNF
from grammaire import Grammaire, Regle
from preprocessing import Processor
from cyk_parser import CYK_PROBA
from nltk.tree import Tree

#%%
# Path to corpus
path = 'sequoia-corpus+fct.mrg_strict'

# Extract train / test / eval trees
train_trees, eval_trees, test_trees = CPFG_CNF.get_trees(path)

# Derive Grammar from training set
grammar = CPFG_CNF.get_grammar(train_trees)

# Get lexicon from training set
lexicon = CPFG_CNF.get_lexicon(train_trees)


# Stores the test trees for testing
f = open('test_chomsky_ter.txt', 'w+')

# Stores the corresponding tokenized sentences
f_sent = open('test_sentence_ter.txt', 'w+')

test_sentence = []

for tree in test_trees:

    chom = re.sub(r'\n\s+', ' ', str(tree))
    f.write(chom +  "\n")

    sent = CPFG_CNF.decode_tree(tree)
    test_sentence.append(sent)


    f_sent.write(sent + "\n")

f.close()
f_sent.close()


# Stores the eval trees for potential future use
f = open('eval_chomsky_ter.txt', 'w+')
for tree in eval_trees:

    chom = re.sub(r'\n\s+', ' ', str(tree))
    f.write(chom +  "\n")
f.close()


#%%

# Build Grammaire
grammaire = Grammaire(grammar, lexicon)

# Build Processor
processor = Processor(lexicon)

# Build CYK parser
cyk = CYK_PROBA(grammaire, processor)

#%%
# Save components for future use

# Saving Grammar 
with open('grammaire_ter', 'wb') as gram_file:
    pickle.dump(grammaire, gram_file)

# Saving Preprocessor
with open('preprocessor_ter', 'wb') as preprocess:
    pickle.dump(processor, preprocess)

# Saving parser
with open('cyk_parser_ter', 'wb') as parser:
    pickle.dump(cyk, parser)

# Saving lexicon
with open('lexicon_ter', 'wb') as lex:
    pickle.dump(lexicon, lex)

# Saving train trees
with open('train_trees_ter', 'wb') as traintress:
    pickle.dump(train_trees, traintress)



#%%

# Load Grammar
with open('grammaire', 'rb') as gram_file:
    grammaire = pickle.load(gram_file)

with open('lexicon', 'rb') as lex:
    lexicon = pickle.load(lex)

with open('preprocessor', 'rb') as preprocess:
    processor = pickle.load(preprocess)


cyk = CYK_PROBA(grammaire, processor)


#%%
# Perform the comparison
(table, dic) = cyk.parse('Le petit chien est parti san son maitre .')
node = cyk.get_best_tree()
a = cyk.build_tree(node, is_root=True)
print(a)

t  = Tree.fromstring(a)
t.pretty_print()

# %%

# Load directly CYK parser
with open('cyk_parser_ter', 'rb') as parser:
    cyk = pickle.load(parser)

#%%

# Create the tesing set of tokenized sentences
f = open('test_sentence_ter.txt', 'r')

test_sentence = []

for sent in f:
    test_sentence.append(sent.rstrip())

f.close()

#%%

(table, dic) = cyk.parse('Le petit chien part sans sa maitresse .')
node = cyk.get_best_tree()
cyk.build_tree(node, is_root=True)

#%%

# Train the model !
f = open('evaluation_data.parser_output_ter.txt', 'w+')

for sentence in test_sentence:
    print(sentence)
    (table, dic) = cyk.parse(sentence)
    node = cyk.get_best_tree()
    print(cyk.build_tree(node, is_root=True) + "\n")
    f.write(cyk.build_tree(node, is_root=True) + "\n")

f.close()

#%%

# Get parsing result

from PYEVALB import scorer
from PYEVALB import parser


# Get test targets
chom_test = []
with open('test_chomsky_ter.txt') as f:
    for sent in f:
        chom_test.append(sent.rstrip())

# Get parsed sentences
chom_gold = []
with open('evaluation_data.parser_output_ter.txt') as f:
    for sent in f:
        chom_gold.append(sent.rstrip())



#%%

# Removing the 'unparsed' sentences
gold = []
test = []

f = open('test_ter.txt', 'w+')
g = open('gold_ter.txt', 'w+')
for i in range(len(chom_gold)):
    print(chom_gold[i])
    if chom_gold[i] != chom_gold[3]:
        gold.append(chom_gold[i].rstrip())

        g.write(chom_gold[i] + '\n')

        test.append(chom_test[i].rstrip())

        f.write(chom_test[i] + '\n')

f.close()
g.close()


# Create scorer
s  = scorer.Scorer()

# Perform the comparision
s.evalb('gold_ter.txt', 'test_ter.txt', 'results_ter.txt')