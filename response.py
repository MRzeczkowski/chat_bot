import random


def get_response(intents_list, intents_json, explain=False):
    tag = intents_list[0]
    list_of_intents = intents_json["intents"]
    for intent in list_of_intents:
        if intent["tag"] == tag:
            response_obj = random.choice(intent["responses"])
            response = response_obj["text"]
            explanation = response_obj.get(
                "explanation", "No explanation available.")
            return response, explanation if explain else response
