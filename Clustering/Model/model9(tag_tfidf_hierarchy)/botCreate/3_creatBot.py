import json,os
import time

def create_intent(project_id, display_name, training_phrases_parts,message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(request={'parent': parent, 'intent': intent})

    print('Intent created: {}'.format(display_name))
    # print("Intent created: {}".format(response))
def list_intents(project_id):
  global allIntent
  from google.cloud import dialogflow

  intents_client = dialogflow.IntentsClient()

  parent = dialogflow.AgentsClient.agent_path(project_id)

  intents = intents_client.list_intents(request={"parent": parent})

  for intent in intents:
    allIntent.append(str(intent.name[38:]))
      # print("=" * 20)
      # print("Intent name: {}".format(intent.name[38:]))
      # print("Intent display_name: {}".format(intent.display_name))
      # print("Action: {}\n".format(intent.action))
      # print("Root followup intent: {}".format(intent.root_followup_intent_name))
      # print("Parent followup intent: {}\n".format(intent.parent_followup_intent_name))

      # print("Input contexts:")
      # for input_context_name in intent.input_context_names:
      #     print("\tName: {}".format(input_context_name))

      # print("Output contexts:")
      # for output_context in intent.output_contexts:
      #     print("\tName: {}".format(output_context.name))
def delete_intent(project_id, intent_id):
    """Delete intent with the given intent type and intent value."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    intent_path = intents_client.intent_path(project_id, intent_id)

    intents_client.delete_intent(request={"name": intent_path})

with open ("./data/completeWrapUpforBot3.json") as f:
  allIntent = json.load(f)

intentNames = []
for intent in allIntent:
  intent = str(intent)
  intentNames.append(intent)

# for intentName in intentNames:
#   if len(intentName)>100:
#     print(intentName) 

errCreateIntent = set()
project_id = 'subbot9' # mock project id
################## get json key form google cloud #############################################################################################
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= './key/subbot9.json'
################## get json key form google cloud #############################################################################################

count1 = 0
while count1 < 1998:
  currentIntent = intentNames.pop()
  intentList = allIntent[currentIntent]
  # info for create bot
  display_name = intentList["display_name"]
  training_phrases_parts = intentList["training_phrases_parts"]
  message_texts = intentList["message_texts"]
  newMessage_texts = []
  for i in message_texts:
    jsonDesc = json.dumps(i,ensure_ascii=False)
    newMessage_texts.append(jsonDesc)
  
  try:
    create_intent(project_id, display_name, training_phrases_parts, newMessage_texts )
    count1 +=1
    print('count1 = ', count1)
  except:
    print(display_name, " -------------> ERROR count1 = " , count1)
    errCreateIntent.add(display_name)
    intentNames.append(currentIntent)
  finally:
    print('allIntent = ',len(intentNames))

project_id = 'subbot9-3' # mock project id
################## get json key form google cloud #############################################################################################
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= './key/subbot9-3.json'
################## get json key form google cloud #############################################################################################

count2 = 0
while intentNames:
  currentIntent = intentNames.pop()
  intentList = allIntent[currentIntent]
  # info for vreate bot
  display_name = intentList["display_name"]
  training_phrases_parts = intentList["training_phrases_parts"]
  message_texts = intentList["message_texts"]
  newMessage_texts = []
  for i in message_texts:
    jsonDesc = json.dumps(i,ensure_ascii=False)
    newMessage_texts.append(jsonDesc)

  try:
    create_intent(project_id, display_name, training_phrases_parts, newMessage_texts)
    count2 +=1
    print('count2 = ', count2)
  except:
    print(display_name, " -------------> ERROR count2 = " , count2)
    errCreateIntent.add(display_name)
    intentNames.append(currentIntent)
  finally:
    print('allIntent = ',len(intentNames))

print('success intent count: ', count1 + count2)

errList = {"errlist" : list(errCreateIntent)}
with open(f"./data/errIntentCreateModel9_2.json",mode='w') as errsave:
  content = json.dump(errList, errsave, ensure_ascii=False)
