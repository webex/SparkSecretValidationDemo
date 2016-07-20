from itty import *
import urllib2
import json

def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents
    
def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents
    

@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.
    X-Spark-Signature - The header containing the sha1 hash we need to validate
    request.body - the Raw JSON String we need to use to validate the X-Spark-Signature
    """
    raw = request.body
    #Let's create the SHA1 signature 
    #based on the request body JSON (raw) and our passphrase (key)
    hashed = hmac.new(key, raw, hashlib.sha1)
    validatedSignature = hashed.hexdigest()

    print 'validatedSignature', validatedSignature
    print 'X-Spark-Signature', request.headers.get('X-Spark-Signature')
    
    if validatedSignature == request.headers.get('X-Spark-Signature'):

        webhook = json.loads(request.body)
        print webhook['data']['id']
        result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
        result = json.loads(result)
        msg = None
        if webhook['data']['personEmail'] != bot_email:
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name, '')
            if 'batman' in in_message or "whoareyou" in in_message:
                msg = "I'm Batman!"
            elif 'batcave' in in_message:
                message = result.get('text').split('batcave')[1].strip(" ")
                if len(message) > 0:
                    msg = "The Batcave echoes, '{0}'".format(message)
                else:
                    msg = "The Batcave is silent..."
            elif 'batsignal' in in_message:
                print "NANA NANA NANA NANA"
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
            if msg != None:
                print msg
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
        return "true"
    else:
        print "Secret does not match, verboten!"

####CHANGE THESE VALUES#####

#Replace this with the secret phrase you used in the webhook creation
key = "somesupersecretphrase"

bot_email = "yourbot@sparkbot.io"
bot_name = "yourBotDisplayName"
bearer = "BOT BEARER TOKEN HERE"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"

run_itty(server='wsgiref', host='0.0.0.0', port=10010)
