import bktree as bk
import pickle

string = 'data/' + str(3) + 'grams.txt'
with open(string, 'rb') as f:
	dic = pickle.load(f)

asm = set()
for i in dic:
	for j in dic[i]:
		asm.add(j)

bkt = bk.BKTree(bk.levenshtein, asm)

