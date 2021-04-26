import json, os, re
import glob

def cleanComment(commentDesc):
  newComment = commentDesc.replace('&nbsp;',' ')
  newComment = newComment.replace('&amp;;',' ')
  newComment = newComment.replace('&quot;',' ')
  # newComment = commentDesc.replace('<br />','  ')
  newComment = re.sub('<.*?>','',newComment)
  if re.search("คลิกเพื่อดูข้อความที่ซ่อนไว้", newComment):
    print(newComment, '\n', '\n')
  return newComment



allTagGroup = {}
os.chdir("../resultFullLessThan5")
for file in glob.glob("*.json"):
  # print(file[:-5][25:])

  with open(f"../resultFullLessThan5/{file}") as f:
    content = json.load(f)
  
  for tagGroup in content:
    name = str(file[:-5][25:]) + " / "+str(tagGroup)
    allTagGroup[name] = content[tagGroup]

count=0
os.chdir("../resultFull>5")
for file in glob.glob("*.json"):
  # print(file[:-5][21:])

  with open(f"../resultFull>5/{file}") as f:
    content = json.load(f)

  for tagGroup in content:
    name = str(file[:-5][21:]) + " / "+str(tagGroup)
    allTagGroup[name] = content[tagGroup]

print(len(allTagGroup))

for intent in allTagGroup:
  listKratoo = allTagGroup[intent]
  for kratoo in listKratoo:
    comments = kratoo['comments']
    for comment in comments:
      # print(cleanComment(comment['desc']), '\n', '\n')
      cleanCommentDesc = cleanComment(comment['desc'])

# with open("./allTagGroup.json",mode='w') as datasave:
#   content = json.dump(allTagGroup, datasave, ensure_ascii=False)








