import generatingCandidates as gc
import time
import string

def filterByEditDistance(typo, cands, dis):
	newcands = set()
	for i in cands:
		if editDistance(typo, i) <= dis:
			newcands.add(i)
	return newcands

def ed(a, b, i, j, mat, prob):
	if mat[i][j] == -1:
		if min(i, j) == 0:
			mat[i][j] = max(i, j)
		elif (i > 1) and (j > 1) and (a[i - 1] == b[j - 2]) and (a[i - 2] == b[j - 1]):
			temp = ed(a, b, i - 1, j, mat) + 1
			m = i - 1
			n = j
			change = add(a[i], a[i - 1])
			if temp > (ed(a, b, i, j - 1, mat) + 1):
				m = i
				n = j - 1
				change = del(b[j], b[j - 1])
			elif temp > (ed(a, b, i - 1, j - 1, mat) + (1 if (a[i - 1] != b[j - 1]) else 0)):
				m = i - 1
				n = j - 1
				change = (subs(a[i], b[j]) if (a[i - 1] != b[j - 1]) else 1)
			elif temp > (ed(a, b, i - 2, j - 2, mat) + 1):
				m = i - 2
				n = j - 2
				change = revr(a[i], a[i - 1])
			mat[i][j] = temp
			prob[i][j] = prob[m][n] * change
		else:
			temp = ed(a, b, i - 1, j, mat) + 1
			m = i - 1
			n = j
			change = add(a[i])
			if temp > (ed(a, b, i, j - 1, mat) + 1):
				m = i
				n = j - 1
				change = del(b[j])
			elif temp > (ed(a, b, i - 1, j - 1, mat) + (1 if (a[i - 1] != b[j - 1]) else 0)):
				m = i - 1
				n = j - 1
				change = (subs(a[i], b[j]) if (a[i - 1] != b[j - 1]) else 1)
			mat[i][j] = temp
			prob[i][j] = prob[m][n] * change
	return mat[i][j]

def editDistance(a, b):
	mat = [[-1 for x in range(len(b) + 1)] for x in range(len(a) + 1)]
	prob = [[1 for x in range(len(b) + 1)] for x in range(len(a) + 1)]
	for i in range(0, len(a) + 1):
		if i == 0:
			prob[i][0] = 1
		else:
			prob[i][0] = prob[i - 1][0] * add(a[i])

	for j in range(0, len(b) + 1):
		if j == 0:
			prob[0][j] = 1
		else:
			prob[0][j] = prob[0][j - 1] * del(b[j])

	return ed(a, b, len(a), len(b), mat, prob)

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

    addXY = []
    delXY = []
    subXY = []
    revXY = []

    f1 = open(path1, 'r')
    f2 = open(path2, 'r')
    f3 = open(path3, 'r')
    f4 = open(path4, 'r')

    data = f1.read()
    data = data.split('\n')
    del data[-1]
    for i in data:
        addXY.append(i.split())
    
    data = f2.read()
    data = data.split('\n')
    del data[-1]
    for i in data:
        delXY.append(i.split())

    data = f3.read()
    data = data.split('\n')
    del data[-1]
    for i in data:
        subXY.append(i.split())

    data = f4.read()
    data = data.split('\n')
    del data[-1]
    for i in data:
        revXY.append(i.split())

    return addXY, delXY, subXY, revXY

