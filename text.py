import noisychannel as nc
import operator
import trie
import pickle
import time

string = 'data/prior.txt'
with open(string, 'rb') as f:
	prior = pickle.load(f)

def correctWord(input_word):
        input_word = input_word.upper()
	start = time.time()
	cands = trie.search(input_word, 4)
	# print "Got results from trie" + str(len(cands))
	edit = {}
	prob = {}
	for i in cands:
		dis, pro = nc.editDistance(input_word, i[0])
		if dis < 4:
			edit[i[0]] = dis
			prob[(i[0], pro, prior[i[0]])] = pro * prior[i[0]]

	# print "Got the probs"
	sorted_x = sorted(prob.items(), key=operator.itemgetter(1), reverse = True)
	end = time.time()
	#print input_word + '\t',
	normalization = 0
	for i in range(min(5, len(sorted_x))):
		normalization += sorted_x[i][1]
        
        output_dict = {}
        for i in range(min(5, len(sorted_x))):
                 output_dict[sorted_x[i][0][0]] = sorted_x[i][1]/normalization
        return output_dict
        
