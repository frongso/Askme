import json 
import re

from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

from scipy.cluster.hierarchy import ward, dendrogram


stopword = thai_stopwords()
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
  return x not in stopword
def removeStopword (arr):
  somelist = [x for x in arr if notdetermine(x)]
  return somelist
def tokenization(text):
  # token the sentence
  token_text = word_tokenize(text, engine="newmm", keep_whitespace=False)
  return token_text

with open(f'../data/DataTank.json') as f:
  alldata = json.load(f)

titles = []
dataPreProcessings = {}
for kratoo in alldata:
  kratooContent = alldata[kratoo]

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

  titles.append(kratooContent['tid'])

# save datapreprocessing
with open(f"../data/dataPreProcess.json",mode='w') as datasave:
  content = json.dump(dataPreProcessings, datasave, ensure_ascii=False)

print('Data preprocess finish!!!!!!')

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

print('TFIDF finish!!!!!!')

############# Hierarchi #############

dist = 1 - cosine_similarity(tfidf_resutl)

print('start do clustering')
linkage_matrix = ward(dist)
print('finish do clustering')
MAX_COPHENETIC_DIST = max(linkage_matrix[:,2]) * 0.39 # max distance between points 

cut = 3.2
print('start plot')

fig, ax = plt.subplots(figsize=(20, 50))
# ax = dendrogram(linkage_matrix, color_threshold=MAX_COPHENETIC_DIST, orientation="right", leaf_font_size=3 ,labels=titles);
ax = dendrogram(linkage_matrix, color_threshold=MAX_COPHENETIC_DIST, leaf_font_size=3 ,labels=titles);

plt.axhline(y=cut, color='b', linestyle='--')
plt.tight_layout()
plt.savefig('ward_clusters.png', dpi=300) #save figure as ward_clusters
plt.close()

from scipy.cluster.hierarchy import fcluster

labels = fcluster(linkage_matrix, cut, criterion='distance')

labels = labels.tolist()

with open(f'../data/DataTank.json') as f:
  alldata = json.load(f)

result = {}
for numGroup, kratoo in zip(labels, titles):
  if numGroup not in result:
    result[numGroup] = []
    result[numGroup].append(alldata[str(kratoo)])
  else:
    result[numGroup].append(alldata[str(kratoo)])

print(len(result))

# save result datafull
with open(f"../data/dataResultFullContent.json",mode='w') as datasave:
  content = json.dump(result, datasave, ensure_ascii=False)

showResult = {}
for numGroup in result:
  showResult[numGroup] = []
  for kI in result[numGroup]:
    showResult[numGroup].append(kI['title']+' '+kI['desc'])

# save result datashow
with open(f"../data/dataResultShow.json",mode='w') as datasave:
  content = json.dump(showResult, datasave, ensure_ascii=False)

# pairs = pd.DataFrame({'labels' : labels, 'doc': titles})

# for i in pairs:
#   print(i)


# plt.tick_params(\
#     axis= 'x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom='off',      # ticks along the bottom edge are off
#     top='off',         # ticks along the top edge are off
#     labelbottom='off')

# plt.tight_layout() #show plot with tight layout
# plt.savefig('ward_clusters.png', dpi=300) #save figure as ward_clusters
# plt.close()






