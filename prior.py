import pickle
fp = open("data/count_1w100k.txt", 'r')
data = fp.read()
fp.close()
dic = {}
splitdata = data.split('\n')
numOfWords = len(splitdata) - 1
prior = {}
counts = {}
total = 0
words = []
for i in range(0, numOfWords):
	temp = splitdata[i].split('\t')
	words.append(temp[0])
	prior[temp[0]] = 0
	counts[temp[0]] = 0

fp = open("data/count_1w.txt", 'r')
data = fp.read()
fp.close()
splitdata = data.split('\n')
numOfWords = len(splitdata) - 1

for i in range(0, numOfWords):
	temp = splitdata[i].split('\t')
	count = int(temp[1])
	counts[temp[0]] = count
	total += count
print "Prior len " + str(len(prior))
for i in prior:
	prior[i] = (counts[i] + 0.5) / (total + 0.5 * len(prior))

string = "data/prior.txt"
with open(string, 'wb') as f:
	pickle.dump(prior, f)
