import random


def get_response(intents_list, intents_json):
    tag = intents_list[0]
    list_of_intents = intents_json["intents"]
    for intent in list_of_intents:
        if intent["tag"] == tag:
            response_obj = random.choice(intent["responses"])
            response = response_obj["text"]
            explanation = response_obj.get(
                "explanation", "Beyond words, it stands self-evident, needing no further elucidation.")
            return response, explanation
