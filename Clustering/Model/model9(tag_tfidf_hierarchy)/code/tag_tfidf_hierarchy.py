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

with open (f"../data/DataTank.json") as f:
  alldata = json.load(f)

needTagPrior1 = [
  "ipad air",
  "ipad mini",
  "ipad pro",
  "ipad pro (2018)",
  "iphone 11",
  "iphone 11 pro",
  "iphone 11 pro max",
  "iphone 4s",
  "iphone 5",
  "iphone 5s",
  "iphone 6",
  "iphone 6 plus",
  "iphone 6s",
  "iphone 6s plus",
  "iphone 7",
  "iphone 7 plus",
  "iphone 8",
  "iphone 8 plus",
  "iphone se",
  "iphone x",
  "iphone xr",
  "iphone xs",
  "iphone xs max",
  "samsung galaxy a30",
  "samsung galaxy a5",
  "samsung galaxy a50",
  "samsung galaxy a7",
  "samsung galaxy a7 (2016)",
  "samsung galaxy a7 (2017)",
  "samsung galaxy a70",
  "samsung galaxy a8",
  "samsung galaxy a80",
  "samsung galaxy a9",
  "samsung galaxy j2",
  "samsung galaxy j7",
  "samsung galaxy j7 core",
  "samsung galaxy j7 prime",
  "samsung galaxy j7 pro",
  "samsung galaxy j7+",
  "samsung galaxy note 10",
  "samsung galaxy note 10+",
  "samsung galaxy note 10.1",
  "samsung galaxy note 3",
  "samsung galaxy note 4",
  "samsung galaxy note 5",
  "samsung galaxy note 7",
  "samsung galaxy note 8",
  "samsung galaxy note 8.0",
  "samsung galaxy note 9",
  "samsung galaxy note edge",
  "samsung galaxy note fan edition",
  "samsung galaxy s10",
  "samsung galaxy s10 plus",
  "samsung galaxy s10e",
  "samsung galaxy s20 ultra 5g",
  "samsung galaxy s3",
  "samsung galaxy s5",
  "samsung galaxy s6",
  "samsung galaxy s6 edge",
  "samsung galaxy s6 edge plus",
  "samsung galaxy s7",
  "samsung galaxy s7 edge",
  "samsung galaxy s8",
  "samsung galaxy s8 plus",
  "samsung galaxy s9",
  "samsung galaxy s9 plus",
  "samsung galaxy tab 7.7",
  "samsung galaxy tab a7 (2016)",
  "samsung galaxy tab e lte",
  "samsung galaxy tab s2",
  "samsung galaxy tab2 10.1",
  "samsung galaxy tab2 7.0",
  "samsung galaxy tabpro s",
  ]
needTagPrior2 = [
    "airpods",
    "apple pencil",
    "apple tv",
    "apple watch",
    "apple watch series 5",
    "asus fonepad",
    "asus zenfone",
    "google pixel",
    "google pixel xl",
    "huawei mate 20 pro",
    "huawei mate 20 x",
    "huawei mediapad",
    "huawei mediapad m3",
    "huawei p20",
    "huawei p20 pro",
    "huawei p30",
    "huawei p30 pro",
    # "huawei smartphone",
    "huawei watch",
    "iphone",
    "ipad",
    "ipod",
    "macbook air",
    "macbook pro",
    "microsoft surface",
    "moto z",
    "nu mobile",
    "oppo a37",
    "oppo f1 plus",
    "oppo f9",
    "oppo find x",
    "oppo r9 plus",
    "samsung galaxy note",
    "samsung galaxy tab",
    "sony a7",
    "sony a7r",
    "vivo nex 3",
    "xiaomi mi 9",
    "xiaomi mipad",
    "xiaomi redmi note 7",
  ]

dataFilterByTagFull = {}
dataFilterByTagShow = {}

for kratoo in alldata:
  kratooContent = alldata[kratoo]

  newTags = []
  for tag in kratooContent['tags']:
    if str(tag).lower() in needTagPrior1:
      newTags.append(str(tag).lower())

  if newTags == []:
    for tag in kratooContent['tags']:
      if str(tag).lower() in needTagPrior2:
        newTags.append(str(tag).lower())
    # print(sorted(newTags))

  if newTags == []:
    print("There is [] tag")

  sortedTag = str(sorted(newTags))
  if sortedTag not in dataFilterByTagFull:
    dataFilterByTagFull[sortedTag] = []
    dataFilterByTagFull[sortedTag].append(kratooContent)
    dataFilterByTagShow[sortedTag] = []
    dataFilterByTagShow[sortedTag].append(kratooContent['title'] + " /// " + kratooContent['desc'])
  else:
    dataFilterByTagFull[sortedTag].append(kratooContent)
    dataFilterByTagShow[sortedTag].append(kratooContent['title'] + " /// " + kratooContent['desc'])

# save result datashow
with open(f"../data/allTag.json",mode='w') as datasave:
  content = json.dump(aa, datasave, ensure_ascii=False)

# save result datashow
with open(f"../data/dataFilterByTagFull.json",mode='w') as datasave:
  content = json.dump(dataFilterByTagFull, datasave, ensure_ascii=False)

# save result datashow
with open(f"../data/dataFilterByTagShow.json",mode='w') as datasave:
  content = json.dump(dataFilterByTagShow, datasave, ensure_ascii=False)

count = 0
for tagsGroup in dataFilterByTagFull:
  listGroup = dataFilterByTagFull[tagsGroup]
  if len(listGroup) == 5:
    count+=1
    # print(tagsGroup, ' -> ', len(listGroup))
print(count)

############## Do ML #######################

with open(f"../data/dataTagGroupCut.json") as data:
  groupCut = json.load(data)

tagGroupCut = {}
for tagsGroup in dataFilterByTagFull:

  listGroup = dataFilterByTagFull[tagsGroup]
  if len(listGroup) <= 5:
    result1Kratoo = { "tagGroup" : str(tagsGroup),
                      "listGroup" : listGroup
                    }

    # save result datashow
    # with open(f"../data/resultFull/FullContentHas1Kratoo{tagsGroup}.json",mode='w') as datasave:
    #   content = json.dump(result1Kratoo, datasave, ensure_ascii=False)

  else:
    # ########################################################################
    # tagGroupCut[tagsGroup] = 1.6
    # ########################################################################
    titles = []
    dataPreProcessings = {}
    for kratooContent in listGroup:
      # preprocessing
      titleDes = kratooContent['title'] + " " + kratooContent['desc']
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
    print('Data preprocess finish  ', tagsGroup)

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

    print('TFIDF finish ', tagsGroup)

    ############# Hierarchi #############

    dist = 1 - cosine_similarity(tfidf_resutl)

    print('start do clustering ', tagsGroup)
    linkage_matrix = ward(dist)
    print('finish do clustering ', tagsGroup)
    MAX_COPHENETIC_DIST = max(linkage_matrix[:,2]) * 0.39 # max distance between points 

    cut = groupCut[str(tagsGroup)]
    print('start plot', tagsGroup)

    fig, ax = plt.subplots(figsize=(20, 50))
    # ax = dendrogram(linkage_matrix, color_threshold=MAX_COPHENETIC_DIST, orientation="right", leaf_font_size=3 ,labels=titles);
    ax = dendrogram(linkage_matrix, color_threshold=MAX_COPHENETIC_DIST, leaf_font_size=4 ,labels=titles);

    plt.axhline(y=cut, color='b', linestyle='--')
    plt.tight_layout()
    plt.savefig(f'../data/pic_plot/ward_clusters_{tagsGroup}.png', dpi=300) #save figure as ward_clusters
    plt.close()

    from scipy.cluster.hierarchy import fcluster

    labels = fcluster(linkage_matrix, cut, criterion='distance')

    labels = labels.tolist()
    print(tagsGroup, " -> ", len(listGroup))
    print(tagsGroup, " -> finish cluster has ", len(labels), " kratoo")

    with open(f'../data/DataTank.json') as f:
      alldata = json.load(f)

    result = {}
    for numGroup, kratoo in zip(labels, titles):
      if numGroup not in result:
        result[numGroup] = []
        result[numGroup].append(alldata[str(kratoo)])
      else:
        result[numGroup].append(alldata[str(kratoo)])

    print(tagsGroup, " -> finish cluster has ",len(result), " cluster")

    # save result datafull
    with open(f"../data/resultFull/dataResultFullContent{tagsGroup}.json",mode='w') as datasave:
      content = json.dump(result, datasave, ensure_ascii=False)

    showResult = {}
    for numGroup in result:
      showResult[numGroup] = []
      for kI in result[numGroup]:
        showResult[numGroup].append(kI['title']+' '+kI['desc'])

    # save result datashow
    with open(f"../data/resultShow/dataResultShowContent{tagsGroup}.json",mode='w') as datasave:
      content = json.dump(showResult, datasave, ensure_ascii=False)

# save result datashow
# with open(f"../data/dataTagGroupCut.json",mode='w') as datasave:
#   content = json.dump(tagGroupCut, datasave, ensure_ascii=False)





















