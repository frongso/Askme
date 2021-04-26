import json

with open(f"../data/clusteringResult.json") as f:
  content = json.load(f)

showResult = {}
for numGrouping in content['listOfWord']:
  showResult[numGrouping] = []
  for kratooContent in content['listOfWord'][numGrouping]:
    showResult[numGrouping].append(kratooContent['title'] + kratooContent['desc'])

with open(f"../data/showAnswerFromCluster.json",mode='w') as datasave:
  content = json.dump(showResult, datasave, ensure_ascii=False)

