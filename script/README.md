### Project Organization

- `cpfg.py`: This module handles the transformation of the train, test and eval sets along with the grammar computation and PCFG derivation.
- `cyk_parser.py` : This module is the one where the parser is built. An other instance Node was created as well to store 1) the start symbol of a given tree 2) its left and right sub-trees (children) and 3) the probability of such a tree.
- `grammaire.py`: This module was added to facilitate the grammar handling on my end. It is composed by an instance Regle that stores both the probability derived form the PCFG module and the left and right symbols composing the rule.
- `preprocessing.py`:This module basically requires an embedding such as polyglot-fr.pkl to be built
- `train.py`: This module performs the training
- `main.py`: This script is the one that is called in the shell file. It allows the user to enter the
following command line:

`python main.py -s ’path_to_sentences’ -p ’path_to_parser’ -f ’path_to_store`

where 1) -s requires the path to a .txt file containing the sentences to be parsed (in string format with exactly 1 whitespace between each token); 2) -p requires the path to the cyk parser to be used to perform the parsing; 3) -f is the path to a `.txt` file where the parsed sentences will be stored.
