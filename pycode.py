import socket
import time
j = "plotter"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5100))
s.listen(1)
conn, addr = s.accept()
print(f"Connected: {conn, addr}")
t = conn.sendall(f"{j}".encode())
conn.close()