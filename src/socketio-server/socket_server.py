import socketio
from aiohttp import web
import io
import base64
from PIL import Image
import re

## creates a new Async Socket IO Server
sio = socketio.AsyncServer(cors_allowed_origins='*')
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

@sio.on('message')
async def print_message(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)
    await sio.emit('message', message[::-1])

@sio.on('image')
async def show_message(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    #message = message[message.find(',') - 1:]
    base64_data = re.sub('^data:image/.+;base64,', '', message)

    b = io.BytesIO(base64.b64decode( base64_data))
    pimg = Image.open(b)
    pimg.show()
    


## We kick off our server
if __name__ == '__main__':
    web.run_app(app)