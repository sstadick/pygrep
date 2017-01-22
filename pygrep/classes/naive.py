from helpers import *

class Naive(object):
    """ Naive Search method
    Starting at the left of the text, attempt to match the leftmost pattern char
    against the corresponding text char. If mismatch, move pattern 1 index to the
    left. If match, add start index of match to matches.
    """

    def __init__(self, pattern):
        self.pattern = pattern


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

if __name__ == '__main__':
    pattern = 'thou'
    text = 'cow th ou cat art hat thou mow the lawn'
    print("Running Naive Search")
    naive = Naive(pattern)
    print("Basic Search")
    print(naive.search(text))
