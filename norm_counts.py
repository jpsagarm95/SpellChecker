import pickle

fp = open('data/count_2l.txt', 'r')
data = fp.read()
fp.close()

splitdata = data.split('\n')
datalen = len(splitdata) - 1

norms1 = {}
norms2 = {}

print "Read Data"

for i in range(0, datalen):
	words = splitdata[i].split('\t')
	str = words[0]
	str = str.upper()
	count = int(words[1])
	norms2[str] = count
	if str[0] in norms1:
		norms1[str[0]] += count
	else:
		norms1[str[0]] = count
	if str[1] in norms1:
		norms1[str[1]] += count
	else:
		norms1[str[1]] = count


print len(norms1)
print len(norms2)

string = 'data/norms1.txt'
with open(string, 'wb') as f:
	pickle.dump(norms1, f)

string = 'data/norms2.txt'
with open(string, 'wb') as f:
	pickle.dump(norms2, f)

print "Done writing into a file"