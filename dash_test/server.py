from time import sleep
import socketio

# create a Socket.IO server
sio = socketio.AsyncServer()

# wrap with ASGI application
app = socketio.ASGIApp(sio)

while True:
    for i in range(2):
        sio.emit('my event', {'data': 'foobar'})
        sleep(2)
