from telebot import TeleBot as Bot
from helpers.conversation import ConversationsStorage, Conversation
from helpers.messaging import parse_manifest, send_until_question
from constants import BOT_TOKEN

bot = Bot(BOT_TOKEN)
welcome, manifest = parse_manifest()
conversations = ConversationsStorage()

@bot.message_handler(commands=["start"])
def on_start(command):
    bot.send_message(command.chat.id, welcome)

@bot.message_handler(content_types=["text"])
def on_message(message):
    uid = message.from_user.id
    prev_answer = message.text

    # if not user: ...

    send = lambda text: bot.send_message(message.chat.id, text)

    if not conversations.exists(uid):
        conversations.add(uid, manifest, default_answers={}) # default_answers=user.convers_answers_data

    conversation = conversations.get(uid)
    conversation, question = send_until_question(send, conversation, prev_answer)

    if (not question) or conversation.answers.stopped:
        # save data

        conversation, _ = send_until_question(send, Conversation(manifest, default_answers={}), None)
        # user.convers_answers_data = {}
    elif not question.skip:
        pass
        # user.convers_answers_data = conversation.answers.data

    conversations.set(uid, conversation)

if __name__ == "__main__":
    print("Bot started!")
    bot.polling()
