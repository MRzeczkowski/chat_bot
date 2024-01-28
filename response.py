import random


def get_responses_exhausted_response(intent_json):
    return random.choice(intent_json["responses_exhausted"])


greeting_intent = "greeting"


def has_already_greeted(context):
    return greeting_intent in context['user_intents']


def get_response(intent, intents_json, context):

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

    intent_data = next(
        (item for item in intents_json["intents"] if item["tag"] == intent), None)
    if intent_data:

        if intent == greeting_intent and has_already_greeted(context):
            return None, get_responses_exhausted_response(intent_data), None, None, None

        responses = intent_data["responses"]
        available_responses = [idx for idx, _ in enumerate(
            responses) if idx not in used_responses.get(intent, [])]

        if not available_responses:
            return None, get_responses_exhausted_response(intent_data), None, None, None

        response_index = random.choice(available_responses)
        response_obj = responses[response_index]
        response = initial_greeting + response_obj["text"]
        explanation = response_obj.get("explanation", None)

        followup_questions = intent_data.get("followup_questions", [])

        if not followup_questions:
            return response_index, response, explanation, None, None

        followup_question_obj = random.choice(followup_questions)
        question = followup_question_obj.get("question", None)
        proposed_intent = followup_question_obj.get("proposed_intent", None)

        return response_index, response, explanation, question, proposed_intent

    return None, "I'm not sure how to respond to that.", None, None, None
