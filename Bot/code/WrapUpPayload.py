import os, glob
import json 

def makePayload(question, answers, count, tid):
  payload = { "display_name" : str(count) + "/" + str(tid),
              "training_phrases_parts" : [question],
              "message_texts" : answers
            }

  return payload

def makeSentence(arr):
  result = ''
  for term in arr:
    result = result + term
  return result

def selectAnswer(comments):
  newlist = sorted(comments, key=lambda k: k['point']+k['emotion'])
  return newlist

with open(f"../dataPreProcess.json") as f:
  allPreprocess = json.load(f)

result = {}
count =  0
for kratoo in allPreprocess:

  question = makeSentence(allPreprocess[kratoo]) # Q to build dialogflow

  with open(f"../dataTank/{kratoo}.json") as file:
    kratooContent = json.load(file)

  # select Answer
  selectedAns = selectAnswer(kratooContent['comments'])

  if not selectedAns:
    continue

  answers = []
  selectedAns = selectedAns[:3]
  for answer in selectedAns:
    answers.append(answer['desc'])
  tid = kratoo
  payload = makePayload(question, answers, count, tid)
  # print(payload)
  result[count] = payload
  count += 1

with open(f"../dataPayload.json",mode='w') as datasave:
  content = json.dump(result, datasave, ensure_ascii=False)




