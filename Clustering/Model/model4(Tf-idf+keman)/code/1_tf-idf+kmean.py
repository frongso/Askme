import json 
import os, glob
import re

from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords

from pythainlp.corpus.common import thai_words

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import numpy as np
import numpy.matlib

np.seterr(divide='ignore', invalid='ignore')

def findBestK(resultKmean):
  Sum_of_squared_distances = []
  for knum in resultKmean:
    Sum_of_squared_distances.append(resultKmean[knum]['Sum_of_squared_distances'])

  # ------find best k----------------------
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
    return idxOfBestPoint
  except:
    print(' cant find best k')
# function for preprocessing
word = thai_stopwords()
def clean_tag(text):
  text = re.sub('<.*?>','',text)
  return text
def complete_clean(text :str):

  # Table for emoticon
  emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002500-\U00002BEF"  # chinese char
                            u"\U00002702-\U000027B0"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"  # dingbats
                            u"\u3030"
                            "]+", flags=re.UNICODE)

  # clean paunsuation
  nopunc_text = re.sub(r"[·“”\"\\,@\'?\$%_\[\]()/*+<=>!`~{|}^:;,-.&#]", "", text, flags=re.I)

  # clean emoticon
  clean_text = emoji_pattern.sub(r'', nopunc_text)

  # clean tag html
  cleantext_text = clean_tag(clean_text)

  return cleantext_text
def notdetermine(x):
  return x not in word
def removeStopword (arr):
  somelist = [x for x in arr if notdetermine(x)]
  return somelist
def tokenization(text):
  # token the sentence
  token_text = word_tokenize(text, engine="newmm", keep_whitespace=False)
  return token_text

dataPreProcessings = {}
os.chdir("../DataTank/")
for file in glob.glob('*.json'):

  # load json of kratoo content
  with open(f"../DataTank/{file}") as f:
    kratooContent = json.load(f)

  # preprocessing
  titleDes = kratooContent['title']
    # clean process
  CleanTxt = complete_clean(titleDes)
  # data token 
  dataToken = tokenization(CleanTxt)
  # remove stop word
  bareText = removeStopword(dataToken)

  dataPreProcessing  = kratooContent
  dataPreProcessing['title'] = bareText
  dataPreProcessing['desc'] = ''

  dataPreProcessings[dataPreProcessing['tid']] = dataPreProcessing

# save datapreprocessing
with open(f"../data/dataPreProcess.json",mode='w') as datasave:
  content = json.dump(dataPreProcessings, datasave, ensure_ascii=False)

############# TF-idf #############

listData = []
for kratoo in dataPreProcessings:
  listData.append(dataPreProcessings[kratoo]['title'])

tokens_listData = [','.join(tkn) for tkn in listData]
tfidf = TfidfVectorizer(analyzer=lambda x:x.split(','),)
try:
  tfidf_resutl = tfidf.fit_transform(tokens_listData)
except:
  print('cant do tf-idf')


############# K-mean #############

# Find best K
resultKmean = {}
K = range(1,1001)
for k in K:
  print(k)
  km = KMeans(n_clusters=k).fit(tfidf_resutl)
  result = km.labels_
  print("finish k : ", k)
  resultKmean[str(k)] = {'Sum_of_squared_distances' : int(km.inertia_),
                    'resultClustering' : result.tolist()}

with open(f"../data/dataKmean(1-1000).json",mode='w') as datasave:
  content = json.dump(resultKmean, datasave, ensure_ascii=False)

kmeanAnswer = findBestK(resultKmean)
kmeanAnswer = str(kmeanAnswer)
kmeanFinalAnswer = {"answer" : kmeanAnswer,
                    "listanswer" : resultKmean[kmeanAnswer]
                    }

with open(f"../data/kmeanFinalAnswer(1-1000).json",mode='w') as datasave:
  content = json.dump(kmeanFinalAnswer, datasave, ensure_ascii=False)
