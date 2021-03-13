import socketio
from aiohttp import web
import time
import test

## creates a new Async Socket IO Server
sio = socketio.AsyncServer(cors_allowed_origins='*')
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

@sio.on('message')
async def print_message(sid, message):
    test.print_message(sid, message)
    await sio.emit('message', message[::-1])

@sio.on('image')
async def show_message(sid, message):
    test.show_image(sid, message)


## We kick off our server
if __name__ == '__main__':
    web.run_app(app)