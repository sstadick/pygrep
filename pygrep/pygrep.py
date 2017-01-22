#!/usr/bin/env python

# Skip Loop


# Match Loop

# Shift

# class BoyerMooreSearch:
"""Boyer Moore search implememtation"""

from string

class BoyerMoyer:
    """ Good general pupose searching algorithm for natural language.

    made to behave like fgrep -i
    """
    def __init__(self, pattern: str) -> str:
        self.pattern = pattern.lower()
        self.patternLen = len(pattern)
        self.badCharacterTable = self.preProcessBadCharacters()
        self.goodSuffixTable = self.preProcessGoodSuffix()


    def preProcessBadCharacters(self) -> dict:
        """Create the lookup for bad character matches
        Value = len(pattern) - index(character) - 1
        Returns:
            table- {character: value}
        """
        pattern = list(self.pattern)
        patternLen = len(pattern)

        table = {}
        for index, character in enumerate(pattern):
            if index < patternLen - 1:
                # assign value based on rightmost character
                table[character] = patternLen - index - 1
            elif (index == patternLen - 1) and (character not in table.keys()):
                # Unless it's the last character, then it prefers its leftmost value
                table[character] = patternLen

        table['*'] = patternLen # any letter not in the pattern

        return table

    def preProcessGoodSuffix(self):
        """ """
        pass


    def badCharacterRule(self, index: int, mismatch: str) -> int:
        """Bad character rule:
        Upon mismatch, skip alignments util (a) mismatch becomes a match, or (b) P moves past mismatched character

        Args:
            index- The index at which the mismatch occured
            mismatch- the character from the text that is the mismatch
        Returns:
            skip- The distance to skip down the text
        """
        pass

    def goodSuffixRule(self):
        """Good Suffix rule:
        let t = substring matched by inner loop; skip until (a) there are no mismatches between P an t or (b) P moves past t

        Args:
            index- The index at which the mimatch occured
        Returns:
            skip- The distance to skip down the text
        """
        pass


    def gaililRule(self):
        """ If a match was found, try to move on assumtion of perodicity """
        pass

    # When there is a mismatch, try both rules, use the one that gives the biggest shift

    def search(self, text: str) -> str:
        if len(self.pattern) == 0 or len(text) == 0 or len(text) < len(self.pattern):
            return []

        matches = []
        i = 0 # place tracking variable
        while i < len(text) - len(self.pattern) + 1:
            shift = 1
            misMatched = False
            for j in range(self.patternLen-1, -1, -1):
                if not self.pattern[j] == text[i + j]:
                    skipBC = self.badCharacterRule(j, t[i + j])
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
    pattern = 'tooth'
    b = BoyerMoyer(pattern)
    print(b.badCharacterTable)
    print(b.bad_character_table())
    # print(b.goodSuffixTable)

