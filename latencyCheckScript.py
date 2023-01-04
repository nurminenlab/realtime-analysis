import time, socket

  
# TCP connection setup
print('Connecting to TCP command server...')
global scommand
scommand = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
scommand.connect(('127.0.0.1', 5000))

print('Connecting to TCP waveform server...')
global sSPK
sSPK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSPK.connect(('127.0.0.1', 5002))

scommand.sendall(b'execute clearalldataoutputs')
time.sleep(0.1)


# Run controller for 1 second
ct = time.time()
for i in range(6):
    
    scommand.sendall(b'set runmode run')
    ct = time.time()
    while  time.time() < ct + 1:
        #do nothing 
        pass
    scommand.sendall(b'set runmode stop')
    time.sleep(0.1)