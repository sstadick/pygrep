#!/usr/bin/env python

import string

""" Source code from https://github.com/BenLangmead/ads1-notebooks/blob/master/2.01_BoyerMoore.ipynb """
def z_array(s):
    """ Use Z algorithm (Gusfield theorem 1.4.1) to preprocess s """
    assert len(s) > 1
    z = [len(s)] + [0] * (len(s)-1)
    # Initial comparison of s[1:] with prefix
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            z[1] += 1
        else:
            break
    r, l = 0, 0
    if z[1] > 0:
        r, l = z[1], 1
    for k in range(2, len(s)):
        assert z[k] == 0
        if k > r:
            # Case 1
            for i in range(k, len(s)):
                if s[i] == s[i-k]:
                    z[k] += 1
                else:
                    break
            r, l = k + z[k] - 1, k
        else:
            # Case 2
            # Calculate length of beta
            nbeta = r - k + 1
            zkp = z[k - l]
            if nbeta > zkp:
                # Case 2a: Zkp wins
                z[k] = zkp
            else:
                # Case 2b: Compare characters just past r
                nmatch = 0
                for i in range(r+1, len(s)):
                    if s[i] == s[i - k]:
                        nmatch += 1
                    else:
                        break
                l, r = k, r + nmatch
                z[k] = r - k + 1
    return z


def n_array(s):
    """ Compile the N array (Gusfield theorem 2.2.2) from the Z array """
    return z_array(s[::-1])[::-1]


def big_l_prime_array(p, n):
    """ Compile L' array (Gusfield theorem 2.2.2) using p and N array.
        L'[i] = largest index j less than n such that N[j] = |P[i:]| """
    lp = [0] * len(p)
    for j in range(len(p)-1):
        i = len(p) - n[j]
        if i < len(p):
            lp[i] = j + 1
    return lp


def big_l_array(p, lp):
    """ Compile L array (Gusfield theorem 2.2.2) using p and L' array.
        L[i] = largest index j less than n such that N[j] >= |P[i:]| """
    l = [0] * len(p)
    l[1] = lp[1]
    for i in range(2, len(p)):
        l[i] = max(l[i-1], lp[i])
    return l


def small_l_prime_array(n):
    """ Compile lp' array (Gusfield theorem 2.2.4) using N array. """
    small_lp = [0] * len(n)
    for i in range(len(n)):
        if n[i] == i+1:  # prefix matching a suffix
            small_lp[len(n)-i-1] = i+1
    for i in range(len(n)-2, -1, -1):  # "smear" them out to the left
        if small_lp[i] == 0:
            small_lp[i] = small_lp[i+1]
    return small_lp


def good_suffix_table(p):
    """ Return tables needed to apply good suffix rule. """
    n = n_array(p)
    lp = big_l_prime_array(p, n)
    return lp, big_l_array(p, lp), small_l_prime_array(n)


def good_suffix_mismatch(i, big_l_prime, small_l_prime):
    """ Given a mismatch at offset i, and given L/L' and l' arrays,
        return amount to shift as determined by good suffix rule. """
    length = len(big_l_prime)
    assert i < length
    if i == length - 1:
        return 0
    i += 1  # i points to leftmost matching position of P
    if big_l_prime[i] > 0:
        return length - big_l_prime[i]
    return length - small_l_prime[i]


def good_suffix_match(small_l_prime):
    """ Given a full match of P to T, return amount to shift as
        determined by good suffix rule. """
    return len(small_l_prime) - small_l_prime[1]


def dense_bad_char_tab(p, amap):
    """ Given pattern string and list with ordered alphabet characters, create
        and return a dense bad character table.  Table is indexed by offset
        then by character. """
    tab = []
    nxt = [0] * len(amap)
    for i in range(0, len(p)):
        c = p[i]
        assert c in amap
        tab.append(nxt[:])
        nxt[amap[c]] = i+1
    return tab

class Naive(object):
    """ Naive Search method
    Starting at the left of the text, attempt to match the leftmost pattern char
    against the corresponding text char. If mismatch, move pattern 1 index to the
    left. If match, add start index of match to matches.
    """

    def __init__(self, pattern):
        self.pattern = pattern

    def speedSearch(self, text):
        """ Apply speed-up strategies to naive search """


    def search(self, text):
        """ Search pattern against text
        Args:
            text- the text to be searched for the pattern
        Returns:
            matches - array of start indexes of the matches
        """
        if len(self.pattern) == 0 or len(text) == 0 or len(text) < len(self.pattern):
            return []

        matches = []
        patLen = len(self.pattern)
        textLen = len(text)

        # iter over the text
        for i in range( textLen - patLen + 1 ):
            mismatch = False

            # iter over the pattern, advance one in case of mismatch
            for j in range( patLen ):
                if self.pattern[j] != text[i + j]:
                    mismatch = True
                    break # out of for loop

            if not mismatch and j == patLen -1:
                matches.append(i)

        return matches


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
    # naive = Naive(pattern)
    # print(naive.search(text))
