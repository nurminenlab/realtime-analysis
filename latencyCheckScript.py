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

scommand.sendall(b'get runmode')
time.sleep(0.1)

scommand.sendall(b'get sampleratehertz')
time.sleep(0.1)

scommand.sendall(b'execute clearalldataoutputs')
time.sleep(0.1)

scommand.sendall(b'set a-009.tcpdataoutputenabled true')
scommand.sendall(b'set a-010.tcpdataoutputenabled true')
scommand.sendall(b'set a-011.tcpdataoutputenabled true')
scommand.sendall(b'set a-012.tcpdataoutputenabled true')

time.sleep(0.1)
# Run controller for 1 second
for i in range(6):
    scommand.sendall(b'set runmode run')
    time.sleep(1)
    scommand.sendall(b'set runmode stop')
    time.sleep(0.1)