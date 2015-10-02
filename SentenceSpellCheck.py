import bayesianClassifier as bc
import sys
import operator

fileName = sys.argv[1]
fout = open(fileName.split('.')[0] + "_out." + fileName.split('.')[1], 'wb')

with open(fileName, 'rb') as f:
    for line in f:
        #print(line),
        line = line.replace('\n', '')
        fout.write(line + '\t')
        output = bc.bayesianCheck(line)
        #output_t = sorted(output.items(), key=operator.itemgetter(1), reverse = True)
        ite = 0
        for j in output:
            if ite == 3:
                break
            fout.write(j[0].lower() + '\t' + str(j[1]) + '\t')
            ite += 1
        fout.write('\n')
        #print(output_t)

fout.close()



