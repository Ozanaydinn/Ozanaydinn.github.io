import base64
from PIL import Image
import re

def print_message(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)

def show_image(sid, message):
        ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    #message = message[message.find(',') - 1:]
    base64_data = re.sub('^data:image/.+;base64,', '', message)

    b = io.BytesIO(base64.b64decode( base64_data))
    pimg = Image.open(b)
    pimg.show()
