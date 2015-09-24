import re
import commands
import pickle

files = commands.getoutput('ls | grep "80.occs"')
files = files.split('\n')

confusionSet = {}
contextWords = {}

for f in files:
	
    lines = {}
    ite = 0
    confusionSetTemp = {}
    with open(f) as fileobj:
        for line in fileobj:
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
                    #print(words)
                    #print(range(start,end+1))
                    #print(i)
                    #print(contextWords)
                    #print(a.group(1))
                    if words[i] in contextWords[a.group(1)]:
                        contextWords[a.group(1)][words[i]] += 1
                    else:
                        contextWords[a.group(1)][words[i]] = 1

            else:
                contextWords[a.group(1)] = {}
                for i in range(start,end+1):
                    contextWords[a.group(1)][words[i]] = 1
            
            ite += 1
    b = re.search('(.+)-',f)
    if b:
        confusionSet[b.group(1)] = confusionSetTemp

for cSet in confusionSet:
    counts = {}
    for cWord in confusionSet[cSet]:
        for ctxWord in contextWords[cWord]:
            if ctxWord in counts:
                counts[ctxWord] += contextWords[cWord][ctxWord]
            else:
                counts[ctxWord] = contextWords[cWord][ctxWord]
    sum_set = 0
    for c in confusionSet[cSet]:
        sum_set += confusionSet[cSet][c]

    for ctxWord in counts:
        if (counts[ctxWord] < 10) or (counts[ctxWord] > (sum_set - 10)):
            for cWord in confusionSet[cSet]:
                contextWords[cWord].pop(ctxWord, None)

#print(confusionSet)
#for cSet in confusionSet:
#    print('++++++++++++++++++++++')
#    for cWord in confusionSet[cSet]:
#        print('-----------------')
#        print(cWord)
#        print('-----------------')
#        print(contextWords[cWord])
pickle.dump(confusionSet, open("ConfusionSets.dict", "wb"))
pickle.dump(contextWords, open("ContextWords.dict", "wb"))


