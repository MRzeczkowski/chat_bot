import random


def get_responses_exhausted_response(intent_json):
    return random.choice(intent_json["responses_exhausted"])


def has_greeted(context):
    return "greeting" in context['user_intents']


def get_response(intent, intents_json, context):
    no_explanation_response = "Beyond words, it stands self-evident, needing no further elucidation."

    initial_greeting = "" if not has_greeted(
        context) else "Greetings! Now, to your question: "

    used_responses = context["used_responses"]

    for i, intent_json in enumerate(intents_json["intents"]):
        if intent_json["tag"] == intent:

            if intent == "greeting" and has_greeted(context):
                return None, get_responses_exhausted_response(intent_json), no_explanation_response

            available_responses = [
                idx for idx, _ in enumerate(intent_json["responses"])
                if idx not in used_responses.get(intent, [])
            ]

            if not available_responses:
                return None, get_responses_exhausted_response(intent_json), no_explanation_response

            response_index = random.choice(available_responses)

            response_obj = intent_json["responses"][response_index]
            response = initial_greeting + response_obj["text"]
            explanation = response_obj.get(
                "explanation", no_explanation_response)

            return response_index, response, explanation
