import re
import commands
import pickle
import math
import nltk
import text
import time
start = time.time()
collocs_left = pickle.load(open('data/brown/Collocs_left_pruned.dict', 'rb'))
collocs_right = pickle.load(open('data/brown/Collocs_right_pruned.dict', 'rb'))
confusionSets = pickle.load(open('data/brown/ConfusionSets.dict', 'rb'))
fp = open("data/all-words-cleaned.txt", 'r')
data = fp.read()
fp.close()
splitdata = data.split('\n')
numOfWords = len(splitdata) - 1
dicti = []
for i in range(0, numOfWords):
	temp = splitdata[i].lower()
	dicti.append(temp)

cWords = {}
confCounts = {}
priorConf = {}

for cSet in confusionSets:
    sum_set = 0
    for cWord in confusionSets[cSet]:
        sum_set += confusionSets[cSet][cWord]
        cWords[cWord] = confusionSets[cSet]
    
    for cWord in confusionSets[cSet]:
        priorConf[cWord] = float(confusionSets[cSet][cWord])/float(sum_set)
        confCounts[cWord] = float(confusionSets[cSet][cWord])
end = time.time()
print end - start
#for w in priorConf:
#    print(w+ ' '),
#    print(priorConf[w])

#print(confCounts)
#print(priorConf)
while (True):
    line = raw_input('Enter line:')
    start = time.time()
    line = line.lower()
    line = line.replace('\n', '')
    line = re.sub('[^0-9a-zA-Z ]+', '', line)
    words_ = line.split(' ')
    set_of_words = []
    minprob = 1   
    minidx = 0
    poss_list = {}
    end = time.time()
    print "1 " + str(end - start)
    start = time.time()
    for i in range(0, len(words_)):
        temp = ''
        maxval = 0
        poss = {}
        start_cor = time.time()
        if words_[i] not in dicti:
        	print words_[i]
	        poss = text.correctWord(words_[i])
	else:
        	poss[words_[i]] = 1
        	continue
        end_cor = time.time()
	print "cor " + str(end_cor - start_cor)
        for p in poss:
            if poss[p] > maxval: 
                maxval = poss[p]
                temp = p
        words_[i] = temp
        if minprob > poss[temp]:
            minidx = i
            minprob = poss[temp]
            poss_list = poss
    kter = 0
    print poss_list
    if len(poss_list) == 0:
        set_of_words.append([])
    	for wter in words_:
	    set_of_words[kter].append(wter)
    else:
	    for w in poss_list:
		if (poss_list[w] > 0.2):
		    set_of_words.append([])
		    for wter in words_:
		        set_of_words[kter].append(wter)

		    set_of_words[kter][minidx] = w
		    kter += 1
    end = time.time()
    print "3 " + str(end - start)
    #print(poss_list)
    start = time.time()
    word_tok = nltk.word_tokenize(line)
    pos_tags = nltk.pos_tag(word_tok)
    end = time.time()
    print "4 " + str(end - start)
    for words in set_of_words:
        #print(words)
    
	    for i in range(0, len(words)):
		words[i] = words[i].lower()

	    
	    for i in range(0, len(words)):

		if words[i] in cWords:
		    start = max(0,i-3)
		    end = min(i+3, len(words)-1)
		    
		    left_seq = ''
		                        
		    for j in range(start,i):
		        left_seq = left_seq + pos_tags[j][1] + ','
		        
		    right_seq = ''
		    for j in range(i+1,end+1):
		        right_seq = right_seq + pos_tags[j][1] + ',' 
		       
		    
		    
		    prob = {}
		    
		    confuse = cWords[words[i]]
		    for w in confuse:
		        prob[w] = priorConf[w]
		        if left_seq in collocs_left[w]:
		            val_l = float(collocs_left[w][left_seq]+1)/(confCounts[w] + len(collocs_left[w]))
		        else:
		            val_l = 1
		        
		        if right_seq in collocs_right[w]:
		            val_r = float(collocs_right[w][right_seq]+1)/(confCounts[w] + len(collocs_right[w]))
		        else:
		            val_r = 1
		        
		        prob[w]*=(val_r*val_l)
		            
		        
		    maxval = 0
		    idx = ''
		    #for p in prob:
		    #    print(p + ' '),
		    #    print(prob[p])
		        
		    for k in prob:
		        if prob[k] > maxval: 
		            maxval = prob[k]
		            idx = k
		    #        print(k)

		    words[i] = idx

	    for i in words:
		print i+' ',

	    print

