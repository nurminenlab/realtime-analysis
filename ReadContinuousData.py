import time, socket

print('Connecting to TCP command server...')
scommand = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scommand.connect(('127.0.0.1', 5000))

print('Connecting to TCP waveform server...')
sSPK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSPK.connect(('127.0.0.1', 5002))

scommand.sendall(b'get runmode')

scommand.sendall(b'get sampleratehertz')

scommand.sendall(b'execute clearalldataoutputs')
time.sleep(0.1)

tcpCommandSPKchannel = "set A-007.tcpdataoutputenabledspike true;".encode("utf-8")
scommand.sendall(tcpCommandSPKchannel)
time.sleep(0.1)

scommand.sendall(b'set runmode run')
time.sleep(2)
        
#while True:
        # Read spike data
rawData = sSPK.recv(200000)

print(rawData)