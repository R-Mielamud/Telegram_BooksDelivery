from telebot import TeleBot as Bot
from helpers.conversation import ConversationsStorage, Conversation
from helpers.messaging import parse_manifest, send_until_question
from api import UsersAPI, OrdersAPI, RequisitesAPI, BillsAPI
from constants import BOT_TOKEN

bot = Bot(BOT_TOKEN)
welcome, manifest = parse_manifest()
conversations = ConversationsStorage()

users = UsersAPI()
orders = OrdersAPI()
requisites = RequisitesAPI()
bills = BillsAPI()

@bot.message_handler(commands=["start"])
def on_start(command):
    uid = command.from_user.id
    user = users.get_by_messenger_id(uid)

    if not user:
        users.create(messenger_id=uid, messenger="Telegram")
    elif user.phone:
        users.partial_update(user.id, phone=None)

    bot.send_message(command.chat.id, welcome)

@bot.message_handler(content_types=["text"])
def on_message(message):
    uid = message.from_user.id
    prev_answer = message.text
    user = users.get_by_messenger_id(uid)

    if not user:
        user = users.create(messenger_id=uid, phone=prev_answer, messenger="Telegram")
        prev_answer = None
    elif not user.phone:
        users.partial_update(user.id, phone=prev_answer)
        prev_answer = None

    send = lambda text: bot.send_message(message.chat.id, text)

    if not conversations.exists(uid):
        conversations.add(uid, manifest, default_answers=user.convers_answers_data)

    conversation = conversations.get(uid)
    conversation, question = send_until_question(send, conversation, prev_answer)

    if conversation.answers.stopped:
        users.partial_update(user.id, convers_answers_data={})
        conversation = Conversation(manifest, default_answers={})
    elif not question:
        update_data = {"convers_answers_data": {}}
        action = conversation.answers.get("action")

        if action == "order":
            orders.create(
                books=conversation.answers.get("books"),
                user=user.id
            )
        elif action == "requisites":
            result = requisites.create(
                delivery_name=conversation.answers.get("delivery_name"),
                delivery_phone=conversation.answers.get("delivery_phone"),
                delivery_address=conversation.answers.get("delivery_address"),
                post_service=conversation.answers.get("post_service")
            )
            
            update_data["requisites"] = result.id
        elif action == "bill":
            bills.create(
                amount=conversation.answers.get("amount"),
                comment=conversation.answers.get("comment"),
                user=user.id
            )

        conversation, _ = send_until_question(send, Conversation(manifest, default_answers={}), None)
        users.partial_update(user.id, **update_data)
    elif not question.skip:
        users.partial_update(user.id, convers_answers_data=conversation.answers.data)

    conversations.set(uid, conversation)

if __name__ == "__main__":
    print("Bot started!")
    bot.polling()
