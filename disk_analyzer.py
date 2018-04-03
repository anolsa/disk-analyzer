import numpy
import os
import sys
from scipy.stats import norm

f = open('results.txt', 'w')
f.write('')
f.close()

def diskAnalyze(filename):
    f = open(filename, 'r')
    data = f.readlines()
    f.close()

    splitData = [i.split('\t') for i in data]
    finalData = []
    for i in reversed(splitData):
        if i[1] != 'Picture':
            finalData.append(i)
        else:
            del finalData[-1]        
            break
    finalData.reverse()

    total = 0.0
    hits = 0.0
    misses = 0.0
    fas = 0.0
    rtimes = []
    

    for i, e in enumerate(finalData):
        if e[1] == 'Sound':
            total += 1
        if e[2] == 'standardi' and i < len(finalData)-1:
            if finalData[i+1][1] == 'Response':
                fas += 1
        elif e[2] == 'deviant1':
            if finalData[i+1][1] == 'Response':
                hits += 1
                rtimes.append((int(finalData[i+1][3]) - int(e[3]))/10)
                if finalData[i+2][1] == 'Response':
                    finalData.pop(i+2)
            elif finalData[i+1][1] == 'Sound':
                misses += 1

    if misses == 0:
        misses = 0.5
    deviants = hits + misses
    hitrate = hits/deviants

    if fas == 0:
        fas = 0.5
    standards = total - deviants - fas
    farate = fas/standards

    dprime = norm.ppf(hitrate) - norm.ppf(farate)
                
    if len(rtimes) > 0:
        rTimeMax = max(rtimes)
        rTimeMin = min(rtimes)
        rTimeAvg = float(sum(rtimes)/len(rtimes))
        rTimeStd = numpy.std(rtimes, ddof=1)
    else:
        rTimeMax = 0
        rTimeMin = 0
        rTimeAvg = 0
        rTimeStd = 0
        
    try:
        result = (str(int(rTimeAvg))+'\t'+str(int(rTimeMax))+'\t'+
                  str(int(rTimeMin))+'\t'+str(int(rTimeStd))+'\t'+
                  str(int(rTimeAvg + (rTimeStd * 3)))+ '\t'+
                  str(int(rTimeAvg - (rTimeStd * 3)))+ '\t'+
                  str(dprime)+'\t'+ str(int(hits))+'\t'+ str(int(fas))+'\n')
        return result
    except ValueError:
        result = "CHECK MANUALLY\n"
        return result
    
for filename in os.listdir(sys.path[0]):
    if filename.endswith('.log'):        
        f = open('results.txt', 'a')
        f.writelines(filename[0:9] + '\t' + diskAnalyze(filename))
        f.close()                    
