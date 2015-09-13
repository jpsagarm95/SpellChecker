import generatingCandidates as gc
import time
def filterByEditDistance(typo, cands, dis):
	newcands = set()
	for i in cands:
		if editDistance(typo, i) <= dis:
			newcands.add(i)
	return newcands

def ed(a, b, i, j, mat):
	if mat[i][j] == -1:
		if min(i, j) == 0:
			mat[i][j] = max(i, j)
		elif (i > 1) and (j > 1) and (a[i - 1] == b[j - 2]) and (a[i - 2] == b[j - 1]):
			mat[i][j] = min(ed(a, b, i - 1, j, mat) + 1, ed(a, b, i, j - 1, mat) + 1, ed(a, b, i - 1, j - 1, mat) + (1 if (a[i - 1] != b[j - 1]) else 0), ed(a, b, i - 2, j - 2, mat) + 1)
		else:
			mat[i][j] = min(ed(a, b, i - 1, j, mat) + 1, ed(a, b, i, j - 1, mat) + 1, ed(a, b, i - 1, j - 1, mat) + (1 if (a[i - 1] != b[j - 1]) else 0))
	return mat[i][j]	

def editDistance(a, b):
	mat = [[-1 for x in range(len(b) + 1)] for x in range(len(a) + 1)]
	return ed(a, b, len(a), len(b), mat)

def all(word, nvalue, tol = 3, dis = 2):
	start = time.clock()
	cands = gc.generatingCandidates(word, nvalue)
	newcands = gc.filterByLength(cands, len(word), tol)
	edcands = filterByEditDistance(word, newcands, dis)
	end = time.clock()
	print(end - start)
	return edcands