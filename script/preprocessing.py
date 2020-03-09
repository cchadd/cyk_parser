import pickle
import numpy as np
import re
from operator import itemgetter


class Processor(object):
    
    def __init__(self, lexicon, path_to_embeddings='polyglot-fr.pkl', encoding='latin1'):
        
        words, embeddings = pickle.load(open(path_to_embeddings, 'rb'), encoding=encoding)
        
        # Normalize embeddings
        embeddings /= np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
        
        self.words = words
        self.embeddings = embeddings

        # Special tokens
        self.Token_ID = {"<UNK>": 0, "<S>": 1, "</S>":2, "<PAD>": 3}
        self.ID_Token = {v:k for k,v in self.Token_ID.items()}

        # Map words to indices and vice versa
        self.word_id = {w:i for (i, w) in enumerate(words)}
        self.id_word = dict(enumerate(words))

        # Normalize digits by replacing them with #
        self.Digits = re.compile("[0-9]", re.UNICODE)


    def __find_closest_leven(self, word, lexicon, verbose=False):
        if word in lexicon:
            if verbose:
                print(f"Word '{word}'' already in lexicon")
            return (word, 0.0)
        else:
            scores = [Processor.levenshtein_dist(word, lex_word) for lex_word in lexicon]

            return lexicon[np.argmin(scores)], scores[np.argmin(scores)]


    def __case_normalizer(self, word, dictionary):
      """ In case the word is not available in the vocabulary,
         we can try multiple case normalizing procedure.
         We consider the best substitute to be the one with the lowest index,
         which is equivalent to the most frequent alternative."""
      w = word
      lower = (dictionary.get(w.lower(), 1e12), w.lower())
      upper = (dictionary.get(w.upper(), 1e12), w.upper())
      title = (dictionary.get(w.title(), 1e12), w.title())
      results = [lower, upper, title]
      results.sort()
      index, w = results[0]
      if index != 1e12:
        return w
      return word


    def __normalize(self, word):
        """ Find the closest alternative in case the word is OOV."""
        if not word in self.word_id:
            word = self.Digits.sub("#", word)
        
        if not word in self.word_id:
            word = self.__case_normalizer(word, self.word_id)

        if not word in self.word_id:
            return None
        return word


    def __l2_nearest(self, word_index, k=1):
        """Sorts words according to their Euclidean distance.
           To use cosine distance, embeddings has to be normalized so that their l2 norm is 1."""

        e = self.embeddings[word_index]
        distances = (((self.embeddings - e) ** 2).sum(axis=1) ** 0.5)
        sorted_distances = sorted(enumerate(distances), key=itemgetter(1))
        return zip(*sorted_distances[:k])


    def find_closest(self, word, lexicon, k_neigh=1, verbose=False):
        """
        This method will try to find the closest word withinh the lexicon derived from the 
        grammar. It will first find the closest word within the path_to_embeddings dictionnary 
        using Levenshteing distance to handle misspelling. Then, it will the k_neigh neighbors 
        in the dictionnary using l2-norm. Finally, it will return the closest word to the k_neigh 
        within the lexicon using Levenshtein distance. 

        Inputs:
        -------

        word (str): The word you want to find the closest in the lexicon
        lexicon (list): A list of word in whcih you want to find the closest word
        k_neigh (int): The number of neighbors to consider
        verose (Boolean)
        """
        word_norm = self.__normalize(word)
    
        # If the word is mispelled we compute the levenshtein distance
        if not word_norm:
            if verbose:
                print(f'word {word}  is OOV! --- Trying to find closest word...')
            word_norm, _ = self.__find_closest_leven(word, list(self.word_id.keys()))
        
        # Get index
        word_index = self.word_id[word_norm]
    
        # Compute cosine distance to find the closest neighbour
        indices, distances = self.__l2_nearest(word_index, k_neigh)
        neighbours = [self.id_word[idx] for idx in indices]

        best_score = np.inf
        best_word = None


        for i, (word, distance) in enumerate(zip(neighbours, distances)):
        
            # Compute again the Levenshtein distance from the lexicon
            w, score = self.__find_closest_leven(word, lexicon)

            if score < best_score:
                best_word = w

            if verbose:
                print(i + 1, '\t', w, score)
        return best_word

          
    @classmethod
    def levenshtein_dist(cls, word_1, word_2):
        """
        This method computes the Levenshtein distance between two words
        """
        m = np.zeros((len(word_1), len(word_2)))
        for i in range(len(word_1)):
            m[i, 0] = i
        for j in range(len(word_2)):
            m[0, j] = j
        for i in range(1, len(word_1)):
            for j in range(1, len(word_2)):
                if word_1[i] == word_2[j]:
                    m[i, j] = min(m[i-1, j] + 1, m[i, j - 1] + 1, m[i - 1, j - 1])
                else:
                    m[i, j] = min(m[i-1, j] + 1, m[i, j - 1] + 1, m[i - 1, j - 1] + 1)  
        return m[-1, -1]