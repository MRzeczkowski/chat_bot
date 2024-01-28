import random


def get_responses_exhausted_response(intent_json):
    return random.choice(intent_json["responses_exhausted"])


greeting_intent = "greeting"


def has_already_greeted(context):
    return greeting_intent in context['user_intents']


def get_response(intent, intents_json, context):
    no_explanation_response = "Beyond words, it stands self-evident, needing no further elucidation."

    if not has_already_greeted(context):
        if intent == greeting_intent:
            initial_greeting = ""
        else:
            # Updating context to make sure not to greet again.
            context['user_intents'].append(greeting_intent)
            initial_greeting = "Greetings! Now, to your question: "
    else:
        initial_greeting = ""

    used_responses = context["used_responses"]

    for i, intent_json in enumerate(intents_json["intents"]):
        if intent_json["tag"] == intent:

            if intent == greeting_intent and has_already_greeted(context):
                return None, get_responses_exhausted_response(intent_json), no_explanation_response

            responses = intent_json["responses"]

            available_responses = [
                idx for idx, _ in enumerate(responses)
                if idx not in used_responses.get(intent, [])
            ]

            if not available_responses:
                return None, get_responses_exhausted_response(intent_json), no_explanation_response

            response_index = random.choice(available_responses)

            response_obj = responses[response_index]
            response = initial_greeting + response_obj["text"]
            explanation = response_obj.get(
                "explanation", no_explanation_response)

            return response_index, response, explanation
