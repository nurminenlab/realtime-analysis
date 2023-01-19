import socket
import time
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind(('172.27.85.52', 51007))
s1.listen(1)
conn, addr = s1.accept()
print("connected from ", addr,"to recieve stim_cond")

'''j = "Plotter Ready!"
conn.sendall(f"{j}".encode())'''
#time.sleep(0.001)


s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind(('172.27.85.52', 51008))
s2.listen(1)
conn2, addr2 = s2.accept()
print("connected from ", addr2,"to runtime for INTAN")

'''j1 = "Plotter Ready to recieve runtime"
conn2.sendall(f"{j1}".encode())'''
#time.sleep(0.001)

while True :
    msg = conn.recv(1).decode()
    runtime = conn2.recv(3).decode()

    # receive data stream. it won't accept data packet greater than 1024 bytes
    if not msg or runtime:
        # if data is not received break
        break
    print(msg )
    print(float(runtime))

#    print(int(runtime))

conn.close()
conn2.close()
print("here")
'''this works
    msglen = conn.recv(1024)
    msglen = int.from_bytes(msglen, byteorder='little', signed=False)
    msg = conn.recv(msglen)
    # receive data stream. it won't accept data packet greater than 1024 bytes
    if not msg or msg == 'end':
        # if data is not received break
        break
    print(type(msg))
    print(msg ," here is the msg")
'''