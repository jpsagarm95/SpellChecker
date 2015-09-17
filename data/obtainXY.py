import re
import pickle

dict_del = {}
dict_add = {}
dict_sub = {}
dict_rev = {}

#Typo|Correction
with open('count_1edit.txt') as openfileobj:
    for line in openfileobj:
        a = line.replace('\n','')
        a = re.split('\t|\|', a)
        len1 = len(a[0])
        len2 = len(a[1])
        count = a[2]
        if len1 == 1 and len2 == 1:
            dict_sub[a[0]+a[1]] = count
        elif len1 == 1 and len2 == 2:
            dict_del[a[1]] = count
        elif len1 == 2 and len2 == 1:
            dict_add[a[0]] = count
        else:
            dict_rev[a[1]] = count

pickle.dump(dict_del, open("delXY.txt","wb"))
pickle.dump(dict_add, open("addXY.txt","wb"))
pickle.dump(dict_sub, open("subXY.txt","wb"))
pickle.dump(dict_rev, open("revXY.txt","wb"))
