import itty3
import requests
import json
import hashlib
import hmac

app = itty3.App()

def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = requests.get(url, 
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json",
                                     "Authorization": "Bearer "+bearer})
    contents = request.json()
    return contents

def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = requests.post(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json",
                                     "Authorization": "Bearer "+bearer}, json=data)
    contents = request.json()
    return contents


@app.post('/')
def index(request):
    body="OK"
    """
    When messages come in from the webhook, they are processed here.
    X-Spark-Signature - The header containing the sha1 hash we need to validate
    request.body - the Raw JSON String we need to use to validate the X-Spark-Signature
    """
    raw = request.body
    #Let's create the SHA1 signature
    #based on the request body JSON (raw) and our passphrase (key)
    hashed = hmac.new(key.encode(), raw, hashlib.sha1)
    validatedSignature = hashed.hexdigest()

    print('validatedSignature', validatedSignature)
    print('X-Spark-Signature', request.headers.get('X-Spark-Signature'))

    if validatedSignature == request.headers.get('X-Spark-Signature'):
        webhook = json.loads(request.body)
        url = 'https://webexapis.com/v1/messages/{0}'.format(webhook['data']['id'])
        result = sendSparkGET(url)
        msg = None
        if webhook['data']['personEmail'] != bot_email:
            url = "https://webexapis.com/v1/messages"
            roomId = webhook['data']['roomId']
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name, '')
            if 'batman' in in_message or "whoareyou" in in_message:
                msg = "I'm Batman!"
            elif 'batcave' in in_message:
                message = result.get('text').split('batcave')[1].strip(" ")
                if len(message) > 0:
                    msg = "The Batcave echoes, '{0}'".format(message)
                    data = {"roomId": roomId, "text": msg}
                    sendSparkPOST(url, data)
                else:
                    msg = "The Batcave is silent..."
                    data = {"roomId": roomId, "text": msg}
                    sendSparkPOST(url, data)
            elif 'batsignal' in in_message:
                print("NANA NANA NANA NANA")
                data = {"roomId": roomId, "text": "On the way!", "files": bat_signal}
                sendSparkPOST(url, data)
            else:
                msg = "Try again, Joker!"
                print(msg)
                data = {"roomId": roomId, "text": msg}
                sendSparkPOST(url, data)
        return app.render(request, body)
    else:
        print("Secret does not match, verboten!")

####CHANGE THESE VALUES#####

#Replace this with the secret phrase you used in the webhook creation
key = "somesupersecretphrase"

bot_email = "yourbot@webex.bot"
bot_name = "Your Bot Name"
bearer = "YOUR_BOT_TOKEN"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"

app.run(addr='0.0.0.0', port=10010)
