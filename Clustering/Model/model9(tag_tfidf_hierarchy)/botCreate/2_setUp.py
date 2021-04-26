import json, re
import pandas as pd

def cleanDesc(desc):
  newDesc = desc.replace('&nbsp;',' ')
  newDesc = newDesc.replace('&amp;;',' ')
  newDesc = newDesc.replace('&quot;',' ')
  newDesc = newDesc.replace('&gt;','>')
  newDesc = newDesc.replace('<a href=\"javascript:void(0);\" class=\"spoil-btn\">[Spoil] คลิกเพื่อดูข้อความที่ซ่อนไว้</a><span class=\"spoil-style\" style=\"display:none;\">','*')
  newDesc = newDesc.replace('&gt;','*') 
  newDesc = newDesc.replace('&lt;','*')  
  # newDesc = re.sub('<.*?>','',newDesc)
  newDesc = newDesc.replace('[Spoil] คลิกเพื่อดูข้อความที่ซ่อนไว้',' ')
  return newDesc

def makePayload(questions, answers, name):
  payload = { "display_name" : name,
              "training_phrases_parts" : questions,
              "message_texts" : answers
            }
  return payload

def selectAnswer(comments, name):
  # try:
  df = pd.DataFrame(comments)
  df["SumPointEmotion"] = df.point + df.emotion
  df = df.sort_values(by = ['SumPointEmotion', 'created_time'],ascending = False)
  newlist = df.to_dict('records')
  # except:
  #   print(comments)
  #   newlist = []
  # newlist = sorted(comments, key=lambda k: k['point']+k['emotion'], reverse = True) #####บรรทัดนี้
  newlist = newlist[:3]
  result = []
  for kratoo in newlist:
    desc = cleanDesc(kratoo['desc'])
    nickname = kratoo['nickname']
    link = kratoo['commentlink']
    newComment = {
      "desc" : desc,
      "nickname": nickname,
      "commentlink" : link,
      "intent": name
    }
    # print('point -> ',kratoo['point']+kratoo['emotion'])

    result.append(newComment)
  return result

with open(f"./data/allTagGroup.json") as f:
  alldata = json.load(f)

print(len(alldata))

warapUpforBot = {}
count = 0
countEmptyList = 0
for intent in alldata:
  listQ = alldata[intent]
  # name for intent
  name = intent
  # answer for intent
  comments = []
  # question for intent
  training_phrases_parts = []
  if listQ:
    count += 1
    for eachQ in listQ:
      if len(eachQ['title']+' '+eachQ['desc']) <= 768:
        training_phrases_parts.append(cleanDesc(eachQ['title']+' '+eachQ['desc']))
      else:
        training_phrases_parts.append(cleanDesc(eachQ['title']))
      for comment in eachQ['comments']:
        comments.append(comment)
    if not comments:
      countEmptyList += 1
      continue
    answers = selectAnswer(comments,name)
    warapUpforBot[name] = makePayload(training_phrases_parts, answers, name)

print(len(warapUpforBot))
print(countEmptyList)

with open(f"./data/completeWrapUpforBot3.json",mode='w') as datasave:
  content = json.dump(warapUpforBot, datasave, ensure_ascii=False)

