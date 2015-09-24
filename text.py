import noisychannel as nc
import operator
import trie
import pickle
import time

string = 'data/prior.txt'
with open(string, 'rb') as f:
	prior = pickle.load(f)
while True:
	# print "Please give the word:"
	input = raw_input()
	input = input.upper()
	start = time.time()
	cands = trie.search(input, 4)
	# print "Got results from trie" + str(len(cands))
	edit = {}
	prob = {}
	for i in cands:
		dis, pro = nc.editDistance(input, i[0])
		if dis < 4:
			edit[i[0]] = dis
			prob[(i[0], pro, prior[i[0]])] = pro * prior[i[0]]

	# print "Got the probs"
	sorted_x = sorted(prob.items(), key=operator.itemgetter(1), reverse = True)
	end = time.time()
	print input + '\t',
	normalization = 0
	for i in range(min(10, len(sorted_x))):
		normalization += sorted_x[i][1]

	for i in range(min(10, len(sorted_x))):
		print sorted_x[i][0][0] + '\t' + str(sorted_x[i][1]/ normalization) + '\t',
	print 
	print "TIME TAKEN: " + str(end - start)
	# whole_list = {}
	# value = sorted_x[0][1]
	# for i in range(len(sorted_x)):
	# 	if value != sorted_x[i][1]:
	# 		value = sorted_x[i][1]
	# 	if value not in whole_list:
	# 		whole_list[value] = {}
	# 	else:
	# 		whole_list[value][sorted_x[i][0]] = prob[sorted_x[i][0]] * prior[sorted_x[i][0]]
	# for i in range(value + 1):
	# 	if i in whole_list:
	# 		prob_order = whole_list[i]
	# 		sorted_probs = sorted(prob_order.items(), key=operator.itemgetter(1), reverse = True)
	# 		for i in range(min(5, len(sorted_probs))):
	# 			print sorted_probs[i]
	# prob_order = {}
	# for i in range(min(10, len(sorted_x))):
	#     prob_order[sorted_x[i]] = prob[sorted_x[i][0]] * prior[sorted_x[i][0]]
	# sorted_probs = sorted(prob_order.items(), key=operator.itemgetter(1), reverse = True)
	# for i in range(min(10, len(sorted_x))):
	# 	print sorted_probs[i]
