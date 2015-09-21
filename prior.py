import pickle
fp = open("data/all-words-cleaned.txt", 'r')
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
	temp = splitdata[i].upper()
	words.append(temp)
	prior[temp] = 0
	counts[temp] = 0

print len(prior)

fp = open("data/count_1w.txt", 'r')
data = fp.read()
fp.close()
splitdata = data.split('\n')
numOfWords = len(splitdata) - 1

for i in range(0, numOfWords):
	temp = splitdata[i].upper().split('\t')
	count = int(temp[1])
	counts[temp[0].upper()] = int(count)
	# print temp
	# print count
	total += count

# for i in prior:
# 	if i in counts:
# 		print "HI"

print "Prior len " + str(len(prior))
for i in prior:
	# print i
	prior[i] = (counts[i] + 0.5) / (total + 0.5 * len(prior))
	# print counts[i]

string = "data/prior.txt"
with open(string, 'wb') as f:
	pickle.dump(prior, f)
