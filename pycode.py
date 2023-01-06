import socket
import time
j = "Plotter Ready!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 51005))
s.listen(1)
conn, addr = s.accept()
print("connected from ", conn)
conn.sendall(f"{j}".encode())

while True :
    msg = conn.recv(1024).decode()
    # receive data stream. it won't accept data packet greater than 1024 bytes
    if not msg:
        # if data is not received break
        break
    print(msg)

conn.close()