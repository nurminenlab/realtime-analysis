import socket 

HEADER = 64 
DISCONNECT_MSG = "!"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #ipconfig in cmd
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

stimulus_clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stimulus_clientsocket.connect(ADDR)

#clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#clientsocket1.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length +=b' '*(HEADER - len(send_length))
    stimulus_clientsocket.send(send_length)
    stimulus_clientsocket.send(message)

send("<text><text><text><text><text><text><text><text><text>")
send(DISCONNECT_MSG)