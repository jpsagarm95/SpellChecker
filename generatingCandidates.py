import pickle
import ngrams as ng

def generatingCandidates(word, nvalue):
	toks = ng.tokens(word, nvalue)
	string = 'data/' + str(nvalue) + 'grams.txt'
	with open(string, 'rb') as f:
		dic = pickle.load(f)
	cands = set()
	for i in toks:
		for j in dic[i]:
			cands.add(j)
	return cands


def filterByLength(cands, length, tol):
	up = length + tol
	down = length - tol
	filteredSet = set()
	for i in cands:
		wordlen = len(i)
		if (wordlen < down) or (wordlen > up):
			continue
		filteredSet.add(i)
	return filteredSet