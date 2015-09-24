from nltk.corpus import brown
import math

a = brown.sents(categories=['editorial','reviews','religion','hobbies','lore','belles_lettres','government','learned','fiction','mystery','science_fiction','adventure','romance','humor'])

confusion_sets = [['angel','angle'],['are','our'],['bare','bear'],['buy','by'],['forth','fourth'],['here','hear'],['hole','whole'],['knew','new'],['know','no'],['later','latter'],['meet','meat'],['patience','patients'],['plain','plane'],['presence','presents'],['rain','reign'],['right','write'],['scene','seen'],['threw','thorough','through'],['to','too','two'],['weak','week'],['where','were']]

sent_list = {}

for ll in confusion_sets:
    for w in ll:
        sent_list[w] = []
        

def make_sentence(str_list, c_list):
    sentence = ''
    for word in str_list:
        word = str(word).lower()
        if word == c_list:
            word = '<< '+word+' >>'
        sentence = sentence+word+' '
    return sentence


for sen in a:
    for word in sen:
        for conf_set in confusion_sets:
            for cw in conf_set:
                if word == cw:
                    sent_list[cw].append(make_sentence(sen,cw))
                    

for terms in sent_list:
    sent_list[terms] = list(set(sent_list[terms]))
    
    
for conf in confusion_sets:
        
    file_name = 'data/brown_test/' + conf[0]+'_80'+'.occs'
    file_name1 = 'data/brown_test/' + conf[0]+'_20'+'.occs'

    f = open(file_name,'w')
    f1 = open(file_name1,'w')

    for cword in conf:
    	list_len = len(sent_list[cword])
    	train_size = int(math.ceil(0.8*list_len))
    	  	
    	for c in range(0,train_size,1):
    	    f.write(sent_list[cword][c])
    	    f.write('\n')
    	
    	for c in range(train_size,list_len,1):
    	    f1.write(sent_list[cword][c])
    	    f1.write('\n')
    	
    f.close()    
    f1.close()	    
                

