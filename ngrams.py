import pickle

def tokens(word, nvalue):
	length = len(word)
	toks = []
	for i in range(0, length - nvalue + 1):
		toks.append(word[i:i + nvalue])
	return toks

def ngrams(word, nvalue, dic):
	toks = tokens(word, nvalue)
	for i in toks:
		if i not in dic:
			dic[i] = []
		dic[i].append(word)
			


def main():
	print "Give the value of n:"
	n = int(raw_input())
	fp = open("data/count_1w100k.txt", 'r')
	data = fp.read()
	fp.close()
	dic = {}
	splitdata = data.split('\n')
	numOfWords = len(splitdata) - 1
	words = []

	for i in range(0, numOfWords):
		temp = splitdata[i].split('\t')
		words.append(temp[0])
	# print len(words)
	# i = 0
	for word in words:
		# i+=1
		ngrams(word, n, dic)
	# print i
	# find = set()
	# for i in dic:
	# 	for j in dic[i]:
	# 		find.add(j)
			
	# print len(find)
	print len(dic)
	string = "data/" + str(n) + "grams.txt"
	with open(string, 'wb') as f:
		pickle.dump(dic, f)