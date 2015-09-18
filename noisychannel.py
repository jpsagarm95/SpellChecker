import generatingCandidates as gc
import time
import string
import pickle

addXY = {}
delXY = {}
subXY = {}
revXY = {}
norms1 = {}
norms2 = {}

def filterByEditDistance(typo, cands, dis):
	newcands = set()
	total = 0
	for i in cands:
		dist, prob = editDistance(typo, i)
		total += prob
		if dist <= dis:
			newcands.add(tuple(i, prob))
	updcands = set()
	for i in newcands:
		updcands.add(tuple(i, prob/ total))
	return updcands

def add(a, b):
	global addXY
	str = a + b
	if str in addXY:
		count = (addXY[str] + 1) * 1.0
	else:
		count = 1.0	
	return (count / (norms1[a] + 26))

def dele(a, b):
	global delXY
	str = a + b
	if str in delXY:
		count = (delXY[str] + 1) * 1.0
	else:
		count = 1.0
	value = 0
	if len(str) == 1:
		value = 26
	else:
		value = 676
	return (count / (norms2[str] + value) )

def subs(a, b):
	global subXY
	str = a + b
	if str in subXY:
		# print  "subs: " + subXY[str] + " " + str
		count = (subXY[str] + 1) * 1.0
	else:
		count = 1.0
	return (count / (norms1[b] + 26))

def revr(a, b):
	global addXY
	str = a + b
	if str in revXY:
		count = (revXY[str] + 1) * 1.0
	else:
		count = 1.0
	value = 0
	if len(str) == 1:
		value = 26
	else:
		value = 676
	return (count / (norms2[a + b] + value))

def ed(a, b, i, j, mat, prob):
	if mat[i][j] == -1:
		if min(i, j) == 0:
			mat[i][j] = max(i, j)
		elif (i > 1) and (j > 1) and (a[i - 1] == b[j - 2]) and (a[i - 2] == b[j - 1]):
			temp = ed(a, b, i - 1, j, mat, prob) + 1
			m = i - 1
			n = j
			change = add(a[i - 2], a[i - 1])
			if temp > (ed(a, b, i, j - 1, mat, prob) + 1):
				m = i
				n = j - 1
				temp = ed(a, b, i, j - 1, mat, prob) + 1
				change = dele(b[j - 2], b[j - 1])
			if temp > ((ed(a, b, i - 1, j - 1, mat, prob) + (1 if (a[i - 1] != b[j - 1]) else 0))):
				m = i - 1
				n = j - 1
				temp = (ed(a, b, i - 1, j - 1, mat, prob) + (1 if (a[i - 1] != b[j - 1]) else 0))
				change = (subs(a[i - 1], b[j - 1]) if (a[i - 1] != b[j - 1]) else 1)
			if temp > (ed(a, b, i - 2, j - 2, mat, prob) + 1):
				m = i - 2
				n = j - 2
				temp = (ed(a, b, i - 2, j - 2, mat, prob) + 1)
				change = revr(a[i - 1], a[i - 2])
			mat[i][j] = temp
			prob[i][j] = prob[m][n] * change
		else:
			temp = ed(a, b, i - 1, j, mat, prob) + 1
			m = i - 1
			n = j
			change = add(a[i - 2], a[i - 1])
			if temp > (ed(a, b, i, j - 1, mat, prob) + 1):
				m = i
				n = j - 1
				temp = (ed(a, b, i, j - 1, mat, prob) + 1)
				change = dele(b[j - 2], b[j - 1])
			if temp > ((ed(a, b, i - 1, j - 1, mat, prob) + (1 if (a[i - 1] != b[j - 1]) else 0))):
				m = i - 1
				n = j - 1
				temp = (ed(a, b, i - 1, j - 1, mat, prob) + (1 if (a[i - 1] != b[j - 1]) else 0))
				change = (subs(a[i - 1], b[j - 1]) if (a[i - 1] != b[j - 1]) else 1)
			mat[i][j] = temp
			prob[i][j] = prob[m][n] * change
	return mat[i][j]

def editDistance(a, b):
	# print b
	mat = [[-1 for x in range(len(b) + 1)] for x in range(len(a) + 1)]
	prob = [[1 for x in range(len(b) + 1)] for x in range(len(a) + 1)]
	for i in range(0, len(a) + 1):
		if i == 0:
			prob[i][0] = 1
		elif i == 1:
			prob[i][0] = prob[i - 1][0]# * add("", a[i - 1])
		else:
			prob[i][0] = prob[i - 1][0] * add(a[i - 2], a[i - 1])


	for j in range(0, len(b) + 1):
		if j == 0:
			prob[0][j] = 1
		elif j == 1:
			prob[0][j] = prob[0][j - 1]# * dele("", b[j - 1])
		else:
			prob[0][j] = prob[0][j - 1] * dele(b[j - 2], b[j - 1])

	ed(a, b, len(a), len(b), mat, prob)

	return mat[len(a)][len(b)], prob[len(a)][len(b)]

def all(word, nvalue, tol = 3, dis = 2):
	start = time.clock()
	cands = gc.generatingCandidates(word, nvalue)
	newcands = gc.filterByLength(cands, len(word), tol)
	edcands = filterByEditDistance(word, newcands, dis)
	end = time.clock()
	print(end - start)
	return edcands


def readXY():
	path1 = 'data/addXY.txt'
	path2 = 'data/delXY.txt'
	path3 = 'data/subXY.txt'
	path4 = 'data/revXY.txt'

	global addXY, delXY, subXY, revXY, norms1, norms2

	string = path1
	with open(string, 'rb') as f:
		addXY = pickle.load(f)
	string = path2
	with open(string, 'rb') as f:
		delXY = pickle.load(f)
	string = path3
	with open(string, 'rb') as f:
		subXY = pickle.load(f)
	string = path4
	with open(string, 'rb') as f:
		revXY = pickle.load(f)
	string = 'data/norms1.txt'
	with open(string, 'rb') as f:
		norms1 = pickle.load(f)
	string = 'data/norms2.txt'
	with open(string, 'rb') as f:
		norms2 = pickle.load(f)


readXY()
