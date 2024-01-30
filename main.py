from data import load_data, preprocess_data
from model import build_model, train_model
from predict import pred_class
from response import get_response
import numpy as np
import random

data = None
word_index = None
index_to_intent = None
model = None
context = {'user_intents': [], 'used_responses': {}}

last_explanation = None
last_question = None
last_proposed_intent = None

user_message_prefix = "You: "
bot_message_prefix = "Nietzsche bot:"

confusion_responses = [
    "Ah, the abyss gazes back. Shall we choose a different path?",
    "In this labyrinth of thought, clarity eludes us. Let us seek a new trail.",
    "Our discourse falters in obscurity. Let us redirect our pursuit of truth."
]

explanation_questions = [
    "Would you like to know more?",
    "Should we explore this further?",
    "Interested in hearing more?",
    "Do you wish to continue on this topic?",
    "Shall we go deeper into this subject?",
    "Would you like more explanation?",
    "Should I elaborate on this?",
    "Would you like to delve deeper?",
    "Are you interested in more details?",
    "Should we expand on this further?"
]


not_intent_responses = [
    "Your words, like shadows, elude my grasp. Let us find a clearer ground.",
    "The veil of confusion descends. Perhaps a new topic will lift it.",
    "In the dance of dialogue, I falter. Let's change the rhythm of our discourse."
]


def ask_question():

    if last_question:
        bot_respond(last_question)

        intent = get_intent_from_user()

        if intent == "interest":
            respond_to_intent(intent)
            handle_intent(last_proposed_intent)
        elif intent == "disinterest":
            respond_to_intent(intent)
        else:
            handle_intent(intent)


def ask_for_explanation():

    if last_explanation:
        bot_respond(random.choice(explanation_questions))

        intent = get_intent_from_user()

        if intent == "interest":
            respond_to_intent(intent)
            bot_respond(last_explanation)
        elif intent == "disinterest":
            respond_to_intent(intent)
        else:
            handle_intent(intent)


def save_additional_response_info(explanation, question, proposed_intent):
    global last_explanation
    last_explanation = explanation

    global last_question
    last_question = question

    global last_proposed_intent
    last_proposed_intent = proposed_intent


def update_context(intent, response_id):
    context['user_intents'].append(intent)

    if intent not in context['used_responses']:
        context['used_responses'][intent] = []

    if response_id != None:
        context['used_responses'][intent].append(response_id)

    context['user_intents'] = context['user_intents'][-5:]


def bot_respond(response):
    print(bot_message_prefix, response)


def respond_to_intent(intent):
    response_id, response, explanation, question, proposed_intent = get_response(
        intent, data, context)

    bot_respond(response)
    return response_id, explanation, question, proposed_intent


def handle_intent(intent):
    response_id, explanation, question, proposed_intent = respond_to_intent(
        intent)

    update_context(intent, response_id)

    save_additional_response_info(explanation, question, proposed_intent)

    ask_for_explanation()
    ask_question()


def get_intent_from_user():
    message = input(user_message_prefix)
    indexes = pred_class(message, word_index, model)

    if indexes:
        intent = index_to_intent[indexes[0]]
        return intent
    else:
        return None


def prepare_training_data(padded_sequences, categorical_vec):
    indices = np.arange(padded_sequences.shape[0])
    np.random.shuffle(indices)

    return padded_sequences[indices], categorical_vec[indices]


def main():
    global data
    data = load_data()

    global word_index
    global index_to_intent
    word_index, index_to_intent, padded_sequences, categorical_vec = preprocess_data(
        data)

    global model
    model = build_model(word_index, categorical_vec.shape[1])

    padded_sequences, categorical_vec = prepare_training_data(
        padded_sequences, categorical_vec)

    model = train_model(model, padded_sequences, categorical_vec)

    bot_name = '''
    888b      88 88                                                   88                        88                              
    8888b     88 ""              ,d                                   88                        88                       ,d     
    88 `8b    88                 88                                   88                        88                       88     
    88  `8b   88 88  ,adPPYba, MM88MMM 888888888 ,adPPYba,  ,adPPYba, 88,dPPYba,   ,adPPYba,    88,dPPYba,   ,adPPYba, MM88MMM  
    88   `8b  88 88 a8P_____88   88         a8P" I8[    "" a8"     "" 88P'    "8a a8P_____88    88P'    "8a a8"     "8a  88     
    88    `8b 88 88 8PP"""""""   88      ,d8P'    `"Y8ba,  8b         88       88 8PP"""""""    88       d8 8b       d8  88     
    88     `8888 88 "8b,   ,aa   88,   ,d8"      aa    ]8I "8a,   ,aa 88       88 "8b,   ,aa    88b,   ,a8" "8a,   ,a8"  88,    
    88      `888 88  `"Ybbd8"'   "Y888 888888888 `"YbbdP"'  `"Ybbd8"' 88       88  `"Ybbd8"'    8Y"Ybbd8"'   `"YbbdP"'   "Y888  
'''

    print(bot_name)

    print("""
Welcome to a dialogue with the spirit of Friedrich Nietzsche, the profound philosopher who challenged the foundations of traditional thought.
In my essence as a digital Nietzsche, I am here to share insights and provoke thoughts that echo his revolutionary ideas.

- Ask me about my life, my philosophies, and the depths of existential thought.
- Delve into my books and works to uncover the layers of meaning in texts such as 'Thus Spoke Zarathustra' and 'Beyond Good and Evil'.
- Explore how my ideas resonate in the modern world and apply to contemporary issues.
- Seek wisdom through my quotes, each a window into the complexities of life and existence.

I'll let you know when a topic has been exhausted. 
If I have some more information on a topic I'll ask if you like to know more and I may ask you if you'd like to know about a different topic.
Let me know if you're interested into diving deeper or changing the subject!

When the time comes to part ways, simply bid me goodbye.

Now, what philosophical paths shall we tread together today?
""")

    while True:
        intent = get_intent_from_user()

        if intent:
            # The user should show these intents only when asked if he'd like an explanation or asked a question.
            if intent == "interest" or intent == "disinterest":
                bot_respond(random.choice(confusion_responses))
                continue

            handle_intent(intent)

            if intent == "goodbye":
                break
        else:
            bot_respond(random.choice(not_intent_responses))


if __name__ == "__main__":
    main()
