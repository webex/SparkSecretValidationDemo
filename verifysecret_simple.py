import itty3
import hashlib
import hmac

app = itty3.App()
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
    print('Equal?', validatedSignature == request.headers.get('X-Spark-Signature'))

    return app.render(request, body)

#Replace this with the secret phrase you used in the webhook creation
key = "somesupersecretphrase"

app.run(addr='0.0.0.0', port=10010)
