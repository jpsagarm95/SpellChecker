import text
import sys
import operator

fileName = sys.argv[1]
fout = open(fileName.split('.')[0] + "_out." + fileName.split('.')[1], 'wb')

with open(fileName, 'rb') as f:
    for line in f:
        word = line.replace('\n', '')
        fout.write(word + '\t')
        corrected = text.correctWord_sc(word)
        corrected_t = sorted(corrected.items(), key=operator.itemgetter(1), reverse=True)
        ite = 0
        for j in corrected_t:
            if ite == 10:
                break
            fout.write(j[0].lower() + '\t' + str(j[1]) + '\t')
            ite += 1
        fout.write('\n')

fout.close()
