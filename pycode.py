import socket
import time
# Create a TCP / IP socket
i = 0 # loop counter
j = 45.395 # data to be sent to MATLAB
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 51001))
    s.listen(1)
    conn, addr = s.accept()
    print(f"Connected: {conn, addr}")
while i < 3:
    t = conn.sendall(f"{j}".encode())
    i += 1
    j += 0.6
    time.sleep(5)
    conn.close()