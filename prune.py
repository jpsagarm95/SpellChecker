import pickle

collocs_left = pickle.load(open('data/brown/Collocs_left.dict', 'rb'))
collocs_right = pickle.load(open('data/brown/Collocs_right.dict', 'rb'))
confusionSet = pickle.load(open('data/brown/ConfusionSets.dict', 'rb'))

temp_right = pickle.load(open('data/brown/Collocs_right.dict', 'rb'))
temp_left = pickle.load(open('data/brown/Collocs_left.dict', 'rb'))

for Cset in confusionSet:
    for cword in confusionSet[Cset]:
        for ctxword in temp_left[cword]:
            if(collocs_left[cword][ctxword] < 0):
                collocs_left[cword].pop(ctxword,None)
        for ctxword in temp_right[cword]:
            if(collocs_right[cword][ctxword] < 0):
                collocs_right[cword].pop(ctxword,None)           




for cSet in confusionSet:
    set_temp = set()
    for cWord in confusionSet[cSet]:
        for ctxWord in collocs_left[cWord]:
            if ctxWord not in set_temp:
                set_temp.add(ctxWord)
    
    for cWord in confusionSet[cSet]:
        for key in set_temp:
            if key not in collocs_left[cWord]:
                collocs_left[cWord][key] = 0
                
for cSet in confusionSet:
    set_temp = set()
    for cWord in confusionSet[cSet]:
        for ctxWord in collocs_right[cWord]:
            if ctxWord not in set_temp:
                set_temp.add(ctxWord)
    
    for cWord in confusionSet[cSet]:
        for key in set_temp:
            if key not in collocs_right[cWord]:
                collocs_right[cWord][key] = 0
                
                

print(confusionSet)
for cSet in confusionSet:
    print('++++++++++++++++++++++')
    for cWord in confusionSet[cSet]:
        print('-----------------')
        print(cWord)
        print('-----------------')
        print(collocs_left[cWord])
pickle.dump(collocs_left, open("data/brown/Collocs_left_pruned.dict", "wb"))
pickle.dump(collocs_right, open("data/brown/Collocs_right_pruned.dict", "wb"))
