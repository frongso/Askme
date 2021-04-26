import json

with open(f"../data/kmeanFinalAnswer(1-1000).json") as f:
  clusterByKmean = json.load(f)

with open(f"../data/dataPreProcess.json") as f:
  dataPreProcess = json.load(f)

totalGrouping = clusterByKmean['answer']
clsuterList = clusterByKmean['listanswer']['resultClustering']
listOfEachGroup = {} # {1 : [], 2 : [] ... n : []}


for numGrouping, kratooId in zip(clsuterList, dataPreProcess):
  with open(f"../DataTank/{kratooId}.json") as f:
    kratoocontent = json.load(f)
  if numGrouping not in listOfEachGroup:
    listOfEachGroup[numGrouping] = []
    listOfEachGroup[numGrouping].append(kratoocontent)
  else:
    listOfEachGroup[numGrouping].append(kratoocontent)


showResultCluster = { 'numberGrouping' : totalGrouping,
                      'listOfWord' : listOfEachGroup
}

with open(f"../data/clusteringResult.json",mode='w') as datasave:
  content = json.dump(showResultCluster, datasave, ensure_ascii=False)
