
from watson_developer_cloud import ConversationV1
import telebot
import json

conversation = ConversationV1(
    username='9a55273f-471a-4e22-853e-b7e8dd30ae24',
    password='UQDYKvDGxf2x',
    version='2017-04-21')

bot = telebot.TeleBot("300493308:AAGbRKHtPFyRBbXnvXJcdK7niXF7w9VJD_M")

dict = {}

@bot.message_handler(content_types=['text'])
def respond(message):
	try:
		#bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))
		#print (message)
		username = message.from_user.first_name
		prevContext = {}
		if username in dict:
			prevContext = dict[username]
		response = conversation.message("a91824b1-227e-41f9-9224-32f53750f99f", {'text': message.text}, context = prevContext)
		context = response['context']
		dict[username] = context
		print(json.dumps(response, indent=2))
		data = json.loads(json.dumps(response, indent=2))
		intent = data["intents"][0]["intent"]
		#confidence = data["intents"][0]["confidence"]
		if not data["entities"]:
			output = data["output"]["text"][0]
		else:
			entity = data["entities"][0]["entity"]
			if entity ==  "yes_no":
				value = data["entities"][0]["value"]
				if value == "Yes":
					output = data["output"]["text"][0]
					bot.send_message(message.chat.id, output)
					photo_name = data["output"]["text"][1]
					photo = open("/"+photo_name+".png", 'rb')
					bot.send_photo(message.chat.id, photo)
					
				else:	
					output = data["output"]["text"][1]
			else:		
				output = data["output"]["text"][1]
		
		
		bot.send_message(message.chat.id, output)
		
	except Exception as e:
		print ("Exception is: ")
		print (e)
		bot.send_message(message.chat.id, "لم أفهم مقصدك")
	
 
	
bot.polling()
