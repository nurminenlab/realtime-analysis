import socket 

HEADER = 64 
DISCONNECT_MSG = "!"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #ipconfig in cmd
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
