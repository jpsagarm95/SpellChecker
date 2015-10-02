import re
import commands
import pickle
import math
import nltk
import text
import time
import operator

def collocations(set_of_words):
    global contextWords
    correct = {}
    line = ""
    for eve in set_of_words[0]:
        line = line + " " + eve
    word_tok = nltk.word_tokenize(line)
    pos_tags = nltk.pos_tag(word_tok)
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
		        
	#           for k in prob:
	#               if prob[k] > maxval: 
	#                   maxval = prob[k]
	#                   idx = k
		            
		    #        print(k)
		    normalize = 0
		    for k in prob:
		         normalize += prob[k]

		    for k in prob:
		        prob[k] /= normalize
		    for eve in prob:
		        if eve in correct:
		            correct[eve] += prob[eve]
		        else:
		            correct[eve] = prob[eve]
    return correct



def context(set_of_words):
    global contextWords
    correct = {}
    for words in set_of_words:

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
                    
                #for k in prob:
                #    if prob[k] > maxval: 
                #        maxval = prob[k]
                #        idx = k
                #        print(k)
                normalize = 0
                for k in prob:
                    normalize += prob[k]

                for k in prob:
                    prob[k] /= normalize
                for eve in prob:
                    if eve in correct:
                        correct[eve] += prob[eve]
                    else:
                        correct[eve] = prob[eve]
                

    return correct

contextWords = pickle.load(open('data/brown/ContextWords.dict', 'rb'))
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

#for w in priorConf:
#    print(w+ ' '),
#    print(priorConf[w])

#print(confCounts)
#print(priorConf)

def bayesianCheck(line):
    #print line + '\t',
    usedSpell = False
    line = line.lower()
    line = line.replace('\n', '')
    line = re.sub('[^0-9a-zA-Z ]+', '', line)
    words_ = line.split(' ')
    set_of_words = []
    minprob = 1   
    minidx = 0
    poss_list = {}
    maxprob = 0
    for i in range(0, len(words_)):
        temp = ''
        maxval = 0
        poss = {}

        if words_[i] not in dicti:
            #print words_[i]
            usedSpell = True
            poss = text.correctWord(words_[i])
        else:
            poss[words_[i]] = 1
            continue

        for p in poss:
            if poss[p] > maxval: 
                maxval = poss[p]
                temp = p
        if len(temp) == 0:
            temp = words_[i]
            #poss[temp] = 1
        
        else:
            words_[i] = temp
            if maxprob < poss[temp]:
                maxidx = i
                maxprob = poss[temp]
                poss_list = poss
    kter = 0
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


    con = context(set_of_words)
    col = collocations(set_of_words)
    total = {}
    final = 0
    for eve in con:
            total[eve] = con[eve]
            final += con[eve]
    for eve in col:
            if eve not in total:
                    total[eve] = col[eve]
            else:
                    total[eve] += col[eve]
            final += con[eve]
                    
    for eve in total:
            total[eve] = total[eve]/final
    
    value = 0
    coreve = ""
    if usedSpell:
            for eve in poss_list:
                    if value < poss_list[eve]:
                            value = poss_list[eve]
                            coreve = eve
            #if coreve in total:
            #        temp = cWords[coreve]
            #        for x in temp:
                            #print x + " " + str(total[x])
            sorted_p = sorted(poss_list.items(), key=operator.itemgetter(1), reverse = True)
            #counter = 0
            #output = {}
            #for fin in sorted_p:
            #        if counter == 3:
            #                break
                    #print fin[0] + "\t" + str(fin[1]),
            #        counter += 1
            #        output[fin[0]] = fin[1]
            return sorted_p 
            #print
    else:
            for eve in line:
                    if eve in total:
                            del total[eve]
            sorted_t = sorted(total.items(), key=operator.itemgetter(1), reverse = True)
            #counter = 0

            return sorted_t
            #output = {}
            #for fin in sorted_t:
            #        if counter == 3:
            #                break
            #        output[fin[0]] = fin[1]
                    #print fin[0] + "\t" + str(fin[1]),
            #        counter += 1
            #print
            #return output

#while(True):
#	line = raw_input('Enter line:')
#        output = bayesianCheck(line)
#        print(output)
