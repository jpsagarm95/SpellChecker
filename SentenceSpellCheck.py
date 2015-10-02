import bayesianClassifier as bc
import sys
import operator

fileName = sys.argv[1]
fout = open(fileName.split('.')[0] + "_out." + fileName.split('.')[1], 'wb')

with open(fileName, 'rb') as f:
    for line in f:
        print(line),
        output = bc.bayesianCheck(line)
        output_t = sorted(output.items(), key=operator.itemgetter(1), reverse = True)
        print(output_t)




