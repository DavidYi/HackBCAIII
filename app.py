from flask import Flask, render_template, request, redirect
from twilio.rest import TwilioRestClient
from twilio import twiml
from twilio.rest.lookups import TwilioLookupsClient
from microsofttranslator import Translator
import jinja2
import os

app = Flask(__name__)
ACCOUNT_SID = "AC5710ab4dd464377fc2a0f14704dc25c0" 
AUTH_TOKEN = "616dcf9e1f3aeecce709127c5bac00ee" 
MY_CLIENT_ID = 'hackbca3'
MY_CLIENT_SECRET = 'AwENjKefBWchBJL5hIS0hOQfQmlOQY4Y1BY+Sg7HuPA='


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
translator = Translator(MY_CLIENT_ID, MY_CLIENT_SECRET)
conversations = {}
languageSpoken = {}
supported_languages = {'ar' : ' Arabic','bg' : 'Bulgarian','ca' : 'Catalan','zh-CHS' : 'Chinese (Simplified)',
	'zh-CHT' : 'Chinese (Traditional)','cs' : 'Czech','da' : 'Danish','nl' : 'Dutch','en' : 'English','et' : 'Estonian',
	'fi' : 'Finnish','fr' : 'French','de' : 'German','el' : 'Greek','ht' : 'Haitian Creole','he' : 'Hebrew','hi' : 'Hindi',
	'hu' : 'Hungarian','id' : 'Indonesian','it' : 'Italian','ja' : 'Japanese','ko' : 'Korean','lv' : 'Latvian','lt' : 'Lithuanian',
	'mww' : 'Hmong Daw','no' : 'Norwegian','pl' : 'Polish','pt' : 'Portuguese','ro' : 'Romanian','ru' : 'Russian','sk' : 'Slovak','sl' : 'Slovenian',
	'es' : 'Spanish','sv' : 'Swedish','th' : 'Thai','tr' : 'Turkish','uk' : 'Ukrainian','vi' : 'Vietnamese',
}
supported_languages = {y.lower():x for x,y in supported_languages.iteritems()}

twilioPhone = "15519996857"
language = None
recipient = None

#recieve the text message
@app.route("/", methods=['GET', 'POST'])
def receive():
	global language
	global recipient
	message = request.form["Body"]
	sender = request.form["From"]
	resp = twiml.Response()
	
	if message == "\help":
		message = "\"@@[phone number]\" - choose the recipient of the translated message\n" \
			"\"@+[language]\" - choose the language that you want it to be translated to\n" \
			"\"\lang\" - to see the supported languages\n" \
			"Just send any message in proper english and I will translate it to your wanted" \
			" language and send it to the recipient."
		resp.message(message)
		return str(resp)
	elif message == "\lang":
		message = ""
		for x in supported_languages:
			message += x +': ' + supported_languages[x] + "\n"
		resp.message(message)
		return str(resp)
	elif message[0:2] == "@@":
		try:
			int(message[2:])
			recipient = message[2:]
			message = "You are going to send the message to " + recipient
			
		except ValueError:
			message = message[2:] + " is not a valid phone number. Please submit a new " \
			"and valid phone number beginning with \"@@\". If you need help " \
			"enter \"\help\""
		resp.message(message)
		return str(resp)

	elif message[0:2] == "@+":
		language = message[2:]
		if language not in supported_languages.values():
			message = language + " is not a valid/and or supported language. Please submit a " \
			"new and valid phone number beginning with \"@@\". If you need help " \
			"enter \"\help\""
			resp.message(message)
			return str(resp)
		else:
#			languageSpoken[conversations[sender]] = language
#			languageSpoken[sender] = translator.detect_language(message)
			message = "The language to be translated has changed to "
			for lang, code in supported_languages.iteritems():
				if code == language:
					message += lang
			resp.message(message)
			return str(resp)
	else:
		print(recipient)
		translate(sender, message)


    
def translate(sender, message):
	print(recipient)
	message = translator.translate(message, language)
	send(sender, message)

def send(sender, message):
	message = client.messages.create(to=recipient, from_=twilioPhone,
                                     body = message)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)