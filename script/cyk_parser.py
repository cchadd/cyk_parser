import numpy as np


class Node(object):
    
    def __init__(self, symbol, proba, left_child, right_child=None):
        
        self.symbol = symbol
        self.proba = proba
        self.left_child = left_child
        self.right_child = right_child
        
        
class CYK_PROBA(object):
    
    def __init__(self, grammar, processor):
        """
        CYK parser instance

        Inputs:
        -------

        grammar (Grammaire): The grammaire on which the parser will be based
        processor (Processor): The processor to be used
        """
        self.table = []
        self.grammar = grammar
        self.processor = processor
    
        
    def __preprocess(self, sentence):
        """
        This method ensure that all words are in the grammar or find the closest 
        one if not

        Inputs:
        -------

        sentence -- (string): The sentence to parse should have exactly 1 whitespace 
        between tokens.
        """
        assert isinstance(sentence, str)
        words = sentence.split(' ')

        process_words = []

        for word in words:
            if word not in self.grammar.lexicon:
                w = self.processor.find_closest(word, self.grammar.lexicon, verbose=False)

            else:
                w = word

            process_words.append(w)

        return process_words
            
        
    def parse(self, sentence):
        """
        |  [1, n] |
        | [1, n-1], [2, n] |
        |   ...   ,  ...   , ... |
        |
        |  [1, 1] , [2, 2] , ... , [n, n] |
        |   The   , phrase ,  to ,  parse | 
        """
        print("parsing sentence ... \n")
        words = self.__preprocess(sentence)
        true_words = sentence.split(' ')
        num_words = len(words)

        Obs = dict()
        self.table = [[[] for lenght in range(num_words)] for height in range(num_words)]
        
        # Create the dictionnary to store Non-terminals
        for i in range(num_words):
            for j in range(num_words):
                Obs[(i, j)] = set()
                
        # Loop over Terminals
        for i in range(num_words):
            for rule in self.grammar.rules:
                if rule.rhs_2 is None:
                    A = rule.lhs
                    a = rule.rhs_1
                    if "{}".format(words[i]) == a:
                        Obs[(i, i)] = Obs[(i, i)] | {A}
                        self.table[i][i].append(Node(A, float(rule.prob), true_words[i]))

        # Loop over the number of words

        for d in range(1, num_words):
            for left in range(num_words - d):
                # Fix the depth to d
                right = left + d

                nodes = []

                for k in range(left, right):
                    
                    for rule in self.grammar.rules:
                        if rule.rhs_2:

                            # Collect left symbol
                            X = rule.lhs
                            
                            # Collect right symbols
                            Y, Z = rule.rhs_1, rule.rhs_2

                            # Check the rule has been seen before
                            if Y in Obs[(left, k)] and Z in Obs[(k + 1, right)]:
                                Obs[(left, right)] = Obs[(left, right)] | {X}


                                # # Store candidate nodes
                                nodes.extend([Node(X, float(rule.prob) * float(left_node.proba) * float(right_node.proba), left_node, right_node) \
                                                                for left_node in self.table[left][k] \
                                                                for right_node in self.table[k + 1][right]])
                    
                                # nodes.append([Node(X, float(rule.prob) * float(left_node.proba) * float(right_node.proba), left_node, right_node) \
                                #                                 for left_node in self.table[left][k] \
                                #                                 for right_node in self.table[k + 1][right]])

                if nodes != []:
                    # Store corresponding scores
                    # scores = [float(node.proba) for node in nodes[0]]
                    scores = [float(node.proba) for node in nodes]

                    # Find the node corresponding to the best score
                    index = np.argmax(scores)

                   # Store the corresponding node in table
                    self.table[left][right] = [nodes[index]]

                else:
                    continue


        return self.table, Obs
        

    def get_best_tree(self):
        """
        This function is called to find and return the root node
        corresponding to the best tree found
        """
        best_prob = - np.inf
        best_final_node = None
        for final_node in self.table[0][-1]:
            if float(final_node.proba) >= best_prob:
                best_final_node = final_node
            
        return best_final_node

    
    def build_tree(self, node, is_root=False):
        """
        This function is called to build the tree itself

        Inputs:
        -------

        node -- (Node): The root of the Tree to be built

        """

        if node is None and is_root:
            return "This sentence is not handled by the computed grammar"
        
        if node.right_child is None and is_root:
            return f"({self.grammar.start} ({node.symbol} {node.left_child}))"

        elif node.right_child is None:
            return f"({node.symbol} {node.left_child})"

        elif is_root:
            return f"({self.grammar.start} ({node.symbol} {self.build_tree(node.left_child)} {self.build_tree(node.right_child)}))"

        return f"({node.symbol} {self.build_tree(node.left_child)} {self.build_tree(node.right_child)})"