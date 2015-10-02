import re
import commands
import pickle
import math
import text

contextWords = pickle.load(open('data/brown/ContextWords.dict', 'rb'))
confusionSets = pickle.load(open('data/brown/ConfusionSets.dict', 'rb'))
fp = open("data/all-words-cleaned.txt", 'r')
data = fp.read()
fp.close()
splitdata = data.split('\n')
numOfWords = len(splitdata) - 1
dict = []
for i in range(0, numOfWords):
	temp = splitdata[i].upper()
	dict.append(temp)

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

#for w in priorConf:
#    print(w+ ' '),
#    print(priorConf[w])

#print(confCounts)
#print(priorConf)
while (True):
    line = raw_input('Enter line:')
    line = line.lower()
    line = line.replace('\n', '')
    line = re.sub('[^0-9a-zA-Z ]+', '', line)
    words_ = line.split(' ')
    set_of_words = []
    minprob = 1   
    minidx = 0
    poss_list = {}

    for i in range(0, len(words_)):
        temp = ''
        maxval = 0
        poss = {}
        if words_[i] not in dict:
	        poss = text.correctWord(words_[i])
	else:
        	poss[words_[i]] = 1
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
    for w in poss_list:
        if (poss_list[w] > 0.2):
            set_of_words.append([])
            for wter in words_:
                set_of_words[kter].append(wter)

            set_of_words[kter][minidx] = w
            kter += 1
    #print(poss_list)
    for words in set_of_words:
        #print(words)

        for i in range(0, len(words)):
            words[i] = words[i].lower()

        for i in range(0, len(words)):
                    
            if words[i] in cWords:
                start = max(0,i-3)
                end = min(i+3, len(words)-1)
                context = set()
                for j in range(start, end+1):
                    context.add(words[j])

                prob = {}
                confuse = cWords[words[i]]
                for w in confuse:
                    prob[w] = priorConf[w]
                    for c in context:
                        val = 1
                        if c in contextWords[w]:
                            val = (float(contextWords[w][c])+1)/(1.0*(confCounts[w] + len(contextWords[w])))
                            #val = (float(contextWords[w][c]))
                        else:
                            val = 1 
                        prob[w] *= val
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
                normalize = 0
                for k in prob:
                    normalize += prob[k]

                for k in prob:
                    prob[k] /= normalize
                
                #print(prob)
                words[i] = idx
                
        for i in words:
            print i+' ',
        print
