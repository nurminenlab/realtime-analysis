import socket
import time

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind(('172.27.85.52', 51007))
s1.listen(1)
conn, addr = s1.accept()
print("connected from ", addr,"to recieve stim_cond")


while True :
    msg = conn.recv(1024).decode()
    

    # receive data stream. it won't accept data packet greater than 1024 bytes
    if not msg or msg == 'end':
        # if data is not received break
        break
    print(msg )
    

conn.close()
