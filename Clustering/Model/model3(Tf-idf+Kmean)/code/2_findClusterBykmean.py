import os, json, glob

import numpy as np
import numpy.matlib

with open(f"../data/dataKmean(1-1000).json") as f:
  resultKmean = json.load(f)

Sum_of_squared_distances = []
for knum in resultKmean:
  Sum_of_squared_distances.append(resultKmean[knum]['Sum_of_squared_distances'])

print(Sum_of_squared_distances)

# ------find best k----------------------
answer = 0
try:
  nPoints = len(Sum_of_squared_distances)
  allCoord = np.vstack((range(nPoints), Sum_of_squared_distances)).T
  firstPoint = allCoord[0]
  lineVec = allCoord[-1] - allCoord[0]
  lineVecNorm = lineVec / np.sqrt(np.sum(lineVec**2))
  vecFromFirst = allCoord - firstPoint
  scalarProduct = np.sum(vecFromFirst * np.matlib.repmat(lineVecNorm, nPoints, 1), axis=1)
  vecFromFirstParallel = np.outer(scalarProduct, lineVecNorm)
  vecToLine = vecFromFirst - vecFromFirstParallel
  distToLine = np.sqrt(np.sum(vecToLine ** 2, axis=1))
  idxOfBestPoint = np.argmax(distToLine)
  print(f'Optimum number of cluster by Elbow method: {idxOfBestPoint}')
  answer =  idxOfBestPoint
except:
  print(' cant find best k')

kmeanAnswer = str(answer)
kmeanFinalAnswer = {"answer" : kmeanAnswer,
                    "listanswer" : resultKmean[kmeanAnswer]
                    }

with open(f"../data/kmeanFinalAnswer(1-1000).json",mode='w') as datasave:
  content = json.dump(kmeanFinalAnswer, datasave, ensure_ascii=False)



