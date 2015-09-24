import re
import commands
import pickle
import math

contextWords = pickle.load(open('data/brown/ContextWords.dict', 'rb'))
confusionSets = pickle.load(open('data/brown/ConfusionSets.dict', 'rb'))

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
        
line = raw_input('Enter line\n')
line = line.lower()
line = line.replace('\n', '')
line = re.sub('[^0-9a-zA-Z ]+', '', line)
words = line.split(' ')

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
                    val = (float(contextWords[w][c])+1)
                else:
                    val = 1
                prob[w] *= float(val)/(confCounts[w]+len(contextWords[w]))
        maxval = 0
        idx = ''
        for k in prob:
            if prob[k] > maxval: 
                maxval = prob[k]
                idx = k

        words[i] = k

for i in words:
    print i+' ',

print

