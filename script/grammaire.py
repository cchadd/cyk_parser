"""
Grammaire class with two instances created to a better usage of grammar rules
"""


class Regle(object):
    """
    Class to transorm Productions instances in simpler to use instances
    """
    
    def __init__(self, lhs, rhs_1, rhs_2, prob):
        self.lhs = lhs
        self.rhs_1 = rhs_1
        self.rhs_2 = rhs_2
        self.prob = prob

    def __repr__(self):
        print(f"{self.lhs} -----> {self.rhs_1} {self.rhs_2} ---- {self.prob}")
        return ''


class Grammaire(object):
    """
    Class to transform Grammar instances in simpler to use instances
    """
    
    def __init__(self, grammar, lexicon):
        self.__grammar = grammar
        
        self.rules = []
        self.lexicon = lexicon
        self.start = grammar._start
        
        
        for prod in grammar.productions():

            lhs = str(prod.lhs())
            rhs_1 = str(prod.rhs()[0])
            if len(prod.rhs()) > 1:
                rhs_2 = str(prod.rhs()[1])
            else: 
                rhs_2 = None
                
            proba = str(prod.prob()).replace('[', '').replace(']', '')
            
            self.rules.append(Regle(lhs, rhs_1, rhs_2, proba))

        
    def __repr__(self):
        for rule in self.rules:
            if rule.rhs_2:
                print(f'{rule.lhs} -> {rule.rhs_1} {rule.rhs_2} -- [{rule.prob}]')
            else:
                print(f'{rule.lhs} -> {rule.rhs_1} -- [{rule.prob}]')
        return ''        