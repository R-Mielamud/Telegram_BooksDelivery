from constants import MANIFEST_PATH
import json

def parse_manifest():
    with open(MANIFEST_PATH, "r") as mani_file:
        content = json.load(mani_file)

    manifest = content["manifest"]
    welcome_message = content["welcome"]

    return welcome_message, manifest

def send_until_question(send, conversation, prev_answer):
    question = conversation.get_next_question(prev_answer)

    while question:
        send(question.text)

        if not question.skip:
            break

        question = conversation.get_next_question(prev_answer)

    return conversation, question
