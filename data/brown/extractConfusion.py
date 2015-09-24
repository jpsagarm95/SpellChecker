import re
import commands
import pickle
import math

files = commands.getoutput('ls | grep "80.occs"')
files = files.split('\n')
print(files)
confusionSet = {}
contextWords = {}

check = 0
for f in files:
	
    lines = {}
    ite = 0
    print(f)
    confusionSetTemp = {}
    with open(f) as fileobj:
        for line in fileobj:
            line = line.lower()
            lines[ite] = line.replace('\n', '')
            lines[ite] = re.sub('[^0-9a-zA-Z<> ]+', '', lines[ite])
            a = re.search('<< (.+?) >>', lines[ite])
            if a:
                if a.group(1) in confusionSetTemp:
                    confusionSetTemp[a.group(1)] += 1
                else:
                    confusionSetTemp[a.group(1)] = 1

            temp_line = re.sub('[<>]', '', lines[ite])
            words = temp_line.split()
            #print(a.group(1))
            #print(f)
            loc = words.index(a.group(1))
            start = max(loc-3,0)
            end = min(loc+3,len(words)-1)
            if a.group(1) in contextWords:
                for i in range(start,end+1):
                    if i != loc:
                        if words[i] in contextWords[a.group(1)]:
                            contextWords[a.group(1)][words[i]] += 1
                        else:
                            contextWords[a.group(1)][words[i]] = 1

            else:
                contextWords[a.group(1)] = {}
                for i in range(start,end+1):
                    if i != loc:
                        contextWords[a.group(1)][words[i]] = 1
            
            ite += 1
    b = re.search('(.+)[-_]',f)
    if b:
        confusionSet[b.group(1)] = confusionSetTemp

for cSet in confusionSet:
    counts = {}
    for cWord in confusionSet[cSet]:
        for ctxWord in contextWords[cWord]:
            #if ctxWord == 'have':
            #    print("WOW!!")
            if ctxWord in counts:
                counts[ctxWord] += contextWords[cWord][ctxWord]
            else:
                counts[ctxWord] = contextWords[cWord][ctxWord]
    sum_set = 0

    #for cWord in confusionSet[cSet]:
    #    if 'have' in contextWords[cWord]:
    #        print "HERE!!"

    for c in confusionSet[cSet]:
        sum_set += confusionSet[cSet][c]
    
     
    for ctxWord in counts:
        #print(ctxWord)
        #for cWord in confusionSet[cSet]:
        #    if 'have' in contextWords[cWord]:
        #        print "HERE!!"


        #print("Arrived at: " + ctxWord)
        if (counts[ctxWord] < 10) or (counts[ctxWord] > (sum_set - 10)):
            for cWord in confusionSet[cSet]:
                contextWords[cWord].pop(ctxWord, None)
            #print(counts[ctxWord])
            #print("Deleted: " + ctxWord)
            #counts.pop(ctxWord,None)

        else:
            entropy = 0
            for cWord in confusionSet[cSet]:
                if ctxWord in contextWords[cWord]:
                    #print(contextWords[cWord][ctxWord])
                    #print(counts[ctxWord])
                    p = float(contextWords[cWord][ctxWord])/float(counts[ctxWord])
                    entropy += -p*math.log(p,2)
                else:
                    entropy += 0
            #print("Entropy of %s: %f"%(ctxWord, entropy))
            
            if entropy > 0.9:
                for cWord in confusionSet[cSet]:
                    contextWords[cWord].pop(ctxWord,None)
            
                #counts.pop(ctxWord, None)


print(confusionSet)
for cSet in confusionSet:
    print('++++++++++++++++++++++')
    for cWord in confusionSet[cSet]:
        print('-----------------')
        print(cWord)
        print('-----------------')
        print(contextWords[cWord])


pickle.dump(confusionSet, open("ConfusionSets.dict", "wb"))
pickle.dump(contextWords, open("ContextWords.dict", "wb"))


