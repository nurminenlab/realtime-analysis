import time, socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

def readUint32(array, arrayIndex):
    variableBytes = array[arrayIndex : arrayIndex + 4]
    variable = int.from_bytes(variableBytes, byteorder='little', signed=False)
    arrayIndex = arrayIndex + 4
    return variable, arrayIndex

def readInt32(array, arrayIndex):
    variableBytes = array[arrayIndex : arrayIndex + 4]
    variable = int.from_bytes(variableBytes, byteorder='little', signed=True)
    arrayIndex = arrayIndex + 4
    return variable, arrayIndex

def readUint16(array, arrayIndex):
    variableBytes = array[arrayIndex : arrayIndex + 1]
    variable = int.from_bytes(variableBytes, byteorder='little', signed=False)
    arrayIndex = arrayIndex + 1
    return variable, arrayIndex

def readChar(array, arrayIndex):
    variableBytes = array[arrayIndex : arrayIndex + 5]
    variable = variableBytes.decode()
    arrayIndex = arrayIndex + 5    
    return variable,arrayIndex

print('Connecting to TCP command server...')
scommand = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scommand.connect(('127.0.0.1', 5000))

print('Connecting to TCP waveform server...')
sSPK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSPK.connect(('127.0.0.1', 5002))

scommand.sendall(b'get runmode')
time.sleep(0.1)

scommand.sendall(b'get sampleratehertz')
time.sleep(0.1)

scommand.sendall(b'execute clearalldataoutputs')
time.sleep(0.1)

tcpCommandSPKchannel = "set A-001.tcpdataoutputenabledspike true;".encode("utf-8")
scommand.sendall(tcpCommandSPKchannel)
time.sleep(0.1)

scommand.sendall(b'set runmode run')
#time.sleep(2)

x_timeStampArr = []
y_vals = []

def animate(x):
    rawIndex = 0
    # Read spike data
    rawData = sSPK.recv(200000)
    #scommand.sendall(b'set runmode stop')
    print(rawData)

    magicNumber, rawIndex = readUint32(rawData, rawIndex)

    if magicNumber != 0x3ae2710f:
        raise Exception('Error... magic number incorrect')   

    SPKchannel, rawIndex =readChar(rawData,rawIndex)

    rawTimestamp, rawIndex = readInt32(rawData, rawIndex)
    
    x_timeStampArr.append(rawTimestamp)
    y_vals.append(1)

    print(f'individual time stamp {rawTimestamp}')
    print(f'time stamp array {x_timeStampArr}')
    plt.cla()
    plt.scatter(x_timeStampArr,y_vals,marker="|")


anim = FuncAnimation(plt.gcf(), animate, interval = 1)
plt.tight_layout()
plt.show()


