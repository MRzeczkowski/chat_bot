import random


def get_response(intent, intents_json, context):
    all_responses_used_response = "It seems we have explored all there is on this topic."
    no_explanation_response = "Beyond words, it stands self-evident, needing no further elucidation."

    if intent == "greeting" and "greeting" in context['user_intents']:
        return None, "We've already exchanged pleasantries, but it's good to continue our dialogue.", no_explanation_response

    used_responses = context["used_responses"]

    for i, intent_json in enumerate(intents_json["intents"]):
        if intent_json["tag"] == intent:

            available_responses = [
                idx for idx, _ in enumerate(intent_json["responses"])
                if idx not in used_responses.get(intent, [])
            ]

            if not available_responses:
                return None, all_responses_used_response, no_explanation_response

            response_index = random.choice(available_responses)

            response_obj = intent_json["responses"][response_index]
            response = response_obj["text"]
            explanation = response_obj.get(
                "explanation", no_explanation_response)
            return response_index, response, explanation
