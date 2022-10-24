from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
import time, socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from ctypes import sizeof

from tkinter import Variable
import seaborn as sns
import numpy as np


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


def SpikeDataPerTrial(inputChannelArray):
    channelDict = {channel:[] for channel in inputChannelArray}

    
    for i in range(len(inputChannelArray)):
        time.sleep(0.1)
        tcpCommandSPKchannel ="set "+inputChannelArray[i]+".tcpdataoutputenabledspike true;" 
        tcpCommandSPKchannel = tcpCommandSPKchannel.encode("utf-8")
        scommand.sendall(tcpCommandSPKchannel)

    time.sleep(0.1)

    scommand.sendall(b'set runmode run')
    time.sleep(0.5) # run for 500ms - 0.5s

    rawData = sSPK.recv(200000)
    print(rawData)
    
    scommand.sendall(b'set runmode stop')
    time.sleep(0.1)

    spikeBytesPerBlock = 14

    if len(rawData) % spikeBytesPerBlock != 0:
        raise Exception('An unexpected amount of data arrived that is not an integer multiple of the expected data size per block')

    numBlocks = int((len(rawData) / spikeBytesPerBlock))

    rawIndex = 0 # Index used to read the raw data that came in through the TCP socket
    spikeTimestamp = [] # List used to contain scaled timestamp values in seconds
    spikeCount = 0
    SPKchannelArray =[]

    '''get channel name when dealing with just one channel
    channelName = rawData[4:9]
    print(channelName.decode()) '''

    for block in range(numBlocks):
        # Expect 4 bytes to be TCP Magic Number as uint32.
        # If not what's expected, raise an exception.
        magicNumber, rawIndex = readUint32(rawData, rawIndex)
    
        if magicNumber != 0x3ae2710f:
            raise Exception('Error... magic number incorrect')  
        
        #reading channel that has spike and appending it
        SPKchannel, rawIndex =readChar(rawData,rawIndex)
        if SPKchannel not in SPKchannelArray:
            SPKchannelArray.append(SPKchannel) 

        # Expect 4 bytes to be timestamp as int32.
        rawTimestamp, rawIndex = readInt32(rawData, rawIndex)
        rawTimestamp = round(rawTimestamp/20)
        # appending timestamp to the associated channel in the channel dictionary
        channelDict[SPKchannel].append(rawTimestamp)

        # append timestamp of every spike to the spikeTimestamp list
        spikeTimestamp.append(rawTimestamp)

        #    Expect 1 bytes of spike ID - it's always 1 hence skipping the next line and simply incrementing the rawIndex by 1
        #   spikeID, rawIndex = readUint16(rawData, rawIndex)  
        rawIndex = rawIndex + 1
        # append spikeID of every spike to the spikeIDarray list
        spikeCount = spikeCount + 1
    

    print(f'channels with spike {SPKchannelArray}')
    print(f'total number of spikes {spikeCount}')  
    print("amplifier Timestamps", spikeTimestamp)
    print(channelDict)

    return channelDict


def plotGraph(channelDict,trialCount):

    x1.extend(channelDict['A-001'])
    y1.extend([None if len(channelDict['A-001'])==0 else trialCount for x in range(len(channelDict['A-001']))])
    sc1.set_offsets(np.c_[x1,y1])

    x2.extend(channelDict['A-002'])
    y2.extend([None if len(channelDict['A-002'])==0 else trialCount for x in range(len(channelDict['A-002']))])
    sc2.set_offsets(np.c_[x2,y2])

    x3.extend(channelDict['A-003'])
    y3.extend([None if len(channelDict['A-003'])==0 else trialCount for x in range(len(channelDict['A-003']))])
    sc3.set_offsets(np.c_[x3,y3])

    x4.extend(channelDict['A-004'])
    y4.extend([None if len(channelDict['A-004'])==0 else trialCount for x in range(len(channelDict['A-004']))])
    sc4.set_offsets(np.c_[x4,y4])

    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)


'''plt.figure(2)
    palette = sns.color_palette("dark:violet")
    plt.bar(channelDict.keys(),[len(channelDict[key]) for key in channelDict.keys()],color=palette)
'''
   

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

plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

x1,y1 = [],[]
x2,y2 = [],[]
x3,y3 = [],[]
x4,y4 = [],[]

sc1 = ax1.scatter(x1,y1,marker='|')
plt.setp(ax1, xlim=(0,800), ylim=(0,5))

sc2 = ax2.scatter(x2,y2,marker='|')
plt.setp(ax2, xlim=(0,800), ylim=(0,5))

sc3 = ax3.scatter(x3,y3,marker='|')
plt.setp(ax3, xlim=(0,800), ylim=(0,5))

sc4 = ax4.scatter(x4,y4,marker='|')
plt.setp(ax4, xlim=(0,800), ylim=(0,5))

plt.xlim(0,800)
plt.ylim(0,5)
fig.suptitle('SPIKE Data for channels ')



userIPchannels = ["A-001","A-002","A-003","A-004"]

stimulusComp_Inp = True
while stimulusComp_Inp:
    plotGraph(SpikeDataPerTrial(userIPchannels),1)

    #plotGraph(SpikeDataPerTrial(userIPchannels),2)

    #plotGraph(SpikeDataPerTrial(userIPchannels),3)

    #plotGraph(SpikeDataPerTrial(userIPchannels),4)

    user_input = input("Enter 'q' to quit: ")
    if user_input == 'q':
        break







# Lauri Pseudo codes
'''
#scommand.sendall(b'set runmode run')

while True:
    # wait for stimulus computer to tell when stimuli is on the screen

    # start collecting spikes from Intan
    channelDict = SpikeDataPerTrial(["A-000","A-001","A-002","A-003"])

    # update plot using the code snippets below

# open plots
plt.figure(1)
indx = 0
while not stopped:
    channelDict = SpikeDataPerTrial(["A-000","A-001","A-002","A-003"])
    if indx == 0:
        # line handle
    increment 
    update handle        


'''