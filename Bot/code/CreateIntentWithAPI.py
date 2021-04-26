import os
import json
# set environment vailable for authen ggclound-project
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../serviceAccountKeyDemo1/demo1Key.json"

def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
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

def list_intents(project_id):
    from google.cloud import dialogflow
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    intents = intents_client.list_intents(request={'parent': parent})

    for intent in intents:
        print('=' * 20)
        print('Intent name: {}'.format(intent.name))
        print('Intent display_name: {}'.format(intent.display_name))
        print('Action: {}\n'.format(intent.action))
        print('Root followup intent: {}'.format(
            intent.root_followup_intent_name))
        print('Parent followup intent: {}\n'.format(
            intent.parent_followup_intent_name))

        print('Input contexts:')
        for input_context_name in intent.input_context_names:
            print('\tName: {}'.format(input_context_name))

        print('Output contexts:')
        for output_context in intent.output_contexts:
            print('\tName: {}'.format(output_context.name))

with open(f"../dataPayload.json") as f:
  payload = json.load(f)

with open(f"../errIntentCreate2.json") as f:
  errIntent = json.load(f)

errCreateIntent = []
project_id = # project_id
for count in errIntent['errlist']:
  display_name = payload[count]["display_name"]
  training_phrases_parts = payload[count]["training_phrases_parts"]
  message_texts = payload[count]["message_texts"]

  try:
    create_intent(project_id, display_name, training_phrases_parts, message_texts )
  except:
    print(count, " -------------> ERROR " )
    errCreateIntent.append(count)

errList = {"errlist" : errCreateIntent}
with open(f"../errIntentCreate3.json",mode='w') as errsave:
  content = json.dump(errList, errsave, ensure_ascii=False)





