import json 

with open(f"../data/DataTank.json") as f:
  content = json.load(f)

change = {}
for num in content:
  kratooContent = content[num]
  change[kratooContent['tid']] = kratooContent

# save datapreprocessing
with open(f"../data/dataTank.json",mode='w') as datasave:
  content = json.dump(change, datasave, ensure_ascii=False)
