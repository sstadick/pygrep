import string
from helpers import *


class BoyerMoore(object):
    """ Encapsulates pattern and associated Boyer-Moore preprocessing. """

    def __init__(self, pattern, alphabet=string.ascii_letters + string.whitespace + string.punctuation):
        self.pattern = pattern
        self.patternLen = len(pattern)
        self.alphabet = alphabet

        # Create map from alphabet characters to integers
        self.alphabet_map = {char: i for i, char in enumerate(self.alphabet)}

        # Make bad character rule table
        self.bad_char = dense_bad_char_tab(pattern, self.alphabet_map)
        # Create good suffix rule table
        _, self.big_l, self.small_l_prime = good_suffix_table(pattern)

    def badCharacterRule(self, i, c):
        """ Return # skips given by bad character rule at offset i """
        assert c in self.alphabet_map
        ci = self.alphabet_map[c]
        assert i > (self.bad_char[i][ci]-1)
        return i - (self.bad_char[i][ci]-1)

    def goodSuffixRule(self, i):
        """ Given a mismatch at offset i, return amount to shift
            as determined by (weak) good suffix rule. """
        length = len(self.big_l)
        assert i < length
        if i == length - 1:
            return 0
        i += 1  # i points to leftmost matching position of P
        if self.big_l[i] > 0:
            return length - self.big_l[i]
        return length - self.small_l_prime[i]

    def gaililRule(self):
        """ Return amount to shift in case where P matches T """
        return len(self.small_l_prime) - self.small_l_prime[1]

    def search(self, text):
        if len(self.pattern) == 0 or len(text) == 0 or len(text) < len(self.pattern):
            return []

        matches = []
        i = 0 # place tracking variable
        while i < len(text) - len(self.pattern) + 1:
            shift = 1
            misMatched = False
            for j in range(self.patternLen-1, -1, -1):
                if not self.pattern[j] == text[i + j]:
                    skipBC = self.badCharacterRule(j, text[i + j])
                    skipGS = self.goodSuffixRule(j)
                    shift = max(shift, skipBC, skipGS)
                    misMatched = True
                    break
            if not misMatched:
                matches.append(i)
                skipMatched = self.gaililRule()
                shift = max(shift, skipMatched)
            i += shift

        return matches

if __name__ == '__main__':
    pattern = 'thou'
    text = 'cow th ou cat art hat thou mow the lawn'
    bm = BoyerMoore(pattern)
    # print([char for char in text])
    # print([(i, char) for i, char in enumerate(text)])
    print(bm.search(text))