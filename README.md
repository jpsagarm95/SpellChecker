# SpellChecker

Initial Idea:

 We used assumption that the trigrams from the typo will also be a trigram in the correct word. With this assumption, we created a dictionary of trigrams and listed all the words with the trigrams. 

When we get a typo, we generate all the possible trigrams and obtain the words corresponding to each trigram. This narrows down our search space. Then we narrowed down our space further by assuming that the typo and the correct word are not seperated by more than a specific length. Now, we applied Damerau edit distance on the remaining words to obtain the possible corrections. 

For each of the possible corrections, we can obtain the probabilities by assuming each character mistake is independent. The top few probable corrections will be outputted. 

Refined idea:

The problem with trigrams assumption is that it will not work for cases such as teh <-> the , etc. So we instead construct a Burkhard Keller Tree constructed on the whole dictionary to query for possible corrections. This will ensure that no corrections are missed and is also fast. The probabilities are computed again in the same fashion.


