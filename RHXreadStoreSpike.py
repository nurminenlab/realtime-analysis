from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
import time, socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from ctypes import sizeof

from tkinter import Variable
import seaborn as sns
import numpy as np
from collections import defaultdict

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
    #print(rawData)
    
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
    

    '''print(f'channels with spike {SPKchannelArray}')
    print(f'total number of spikes {spikeCount}')  
    print("amplifier Timestamps", spikeTimestamp)
    print(channelDict)'''

    return channelDict


def plotGraph(channelDict,trialCount):

    x1.extend(channelDict[userIPchannels[0]])
    y1.extend([None if len(channelDict[userIPchannels[0]])==0 else trialCount for x in range(len(channelDict[userIPchannels[0]]))])
    sc[0].set_offsets(np.c_[x1,y1])

    x2.extend(channelDict[userIPchannels[1]])
    y2.extend([None if len(channelDict[userIPchannels[1]])==0 else trialCount for x in range(len(channelDict[userIPchannels[1]]))])
    sc[1].set_offsets(np.c_[x2,y2])

    x3.extend(channelDict[userIPchannels[2]])
    y3.extend([None if len(channelDict[userIPchannels[2]])==0 else trialCount for x in range(len(channelDict[userIPchannels[2]]))])
    sc[2].set_offsets(np.c_[x3,y3])

    x4.extend(channelDict[userIPchannels[3]])
    y4.extend([None if len(channelDict[userIPchannels[3]])==0 else trialCount for x in range(len(channelDict[userIPchannels[3]]))])
    sc[3].set_offsets(np.c_[x4,y4])

    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)  

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

totTimeStampsList = []

plt.ion()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

axes = [ax1,ax2,ax3,ax4] 
# lauri : customize subplot according to channels 
# fig, axes = plt.subplots(nX,nY)

x1,y1 = [],[]
x2,y2 = [],[]
x3,y3 = [],[]
x4,y4 = [],[]

sc = []
for axis,i in zip(axes,range(len(axes))):
    sc.append(axis.scatter([],[],marker='|'))
    plt.setp(axis, xlim=(0,550), ylim=(0,5))
fig.text(0.5, 0.04, 'Timestamps', ha='center', va='center')
fig.text(0.06, 0.5, 'Trials', ha='center', va='center', rotation='vertical')

fig.suptitle('SPIKE Data for channels ')
plt.ylabel("Trials")

userIPchannels = ["A-001","A-002","A-003","A-004"]

stimulusComp_Inp = True
while stimulusComp_Inp:
    
    channelDict = SpikeDataPerTrial(userIPchannels)
    totTimeStampsList.append(channelDict)
    plotGraph(channelDict,1)

    channelDict = SpikeDataPerTrial(userIPchannels)
    totTimeStampsList.append(channelDict)
    plotGraph(channelDict,2)

    channelDict = SpikeDataPerTrial(userIPchannels)
    totTimeStampsList.append(channelDict)
    plotGraph(channelDict,3)

    channelDict = SpikeDataPerTrial(userIPchannels)
    totTimeStampsList.append(channelDict)
    plotGraph(channelDict,4)

    totTimeStamps = defaultdict(list)

    for eachtrial in (totTimeStampsList): # you can list as many input dicts as you want here
        for key, value in eachtrial.items():
            totTimeStamps[key].extend(value)
    
    plt.figure(2)
    palette = sns.color_palette("dark:violet")
    plt.bar(totTimeStamps.keys(),[len(totTimeStamps[key]) for key in totTimeStamps.keys()],color=palette)
    plt.title("no. of spikes vs Channel")
    plt.ylabel("count(SPK)")


    user_input = input("Enter 'q' to quit: ")
    if user_input == 'q':
        
        fig.savefig('plot.png')
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