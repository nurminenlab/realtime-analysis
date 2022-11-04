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
import random

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

    spkC = np.nan * np.ones(len(channelDict))
    for i in range(len(channelDict)):
        spkC[i] = len(channelDict[SPKchannelArray[i]])

    return channelDict, spkC


def plotSPKvsCHNL(channelDict,trialCount):
    for i,xy in zip(range(4),xyArr):
        xy[0].extend(channelDict[userIPchannels[i]])
        xy[1].extend([None if len(channelDict[userIPchannels[i]])==0 else trialCount for x in range(len(channelDict[userIPchannels[i]]))])
        sc[i].set_offsets(np.c_[xy[0],xy[1]])

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.05)  

def plotSPKvsSTIM(stim_cond,SPKcount,y1): #x = stim_cond  y = SPKcount (int)
    x1.append(stim_cond)
    y1 = np.append(y1,SPKcount)
    line1.set_xdata(x1)
    line1.set_ydata(y1)
    fig2.canvas.draw()
    fig2.canvas.flush_events()
    time.sleep(0.1)
    return y1
    
# TCP connection
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

print("opening plot......")
# setting up plot 
plt.ion() # Enable interactive mode for plot

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10, 10))
axes = [ax1,ax2,ax3,ax4] 
# lauri : customize subplot according to channels 
# fig, axes = plt.subplots(nX,nY)

#plot set up for 4 channels and SPKs
xyArr = [([],[]),([],[]),([],[]),([],[])] #for 4 channels (if > 4 Channels , append ([],[]) - note: it should be a tuple)
sc = [] # scatter plot list
for axis,i in zip(axes,range(len(axes))):
    sc.append(axis.scatter([],[],marker='|'))
    plt.setp(axis, xlim=(0,550), ylim=(0,5))
fig.suptitle('SPIKE Data for channels ')
fig.text(0.5, 0.04, 'Timestamps', ha='center', va='center')
fig.text(0.06, 0.5, 'Trials', ha='center', va='center', rotation='vertical')


#plot setup for number of spikes and stim_conditions
x1 = []
y1 = np.array([])
fig2, ax = plt.subplots(figsize=(8, 8))
line1, = ax.plot(x1, y1)
plt.setp(ax, xlim=(0,6), ylim=(0,50))
fig2.suptitle('No. of SPK vs Stimulus conditions')
fig2.text(0.5, 0.04, 'Stimulus conditions', ha='center', va='center')
fig2.text(0.06, 0.5, 'count(SPK)', ha='center', va='center', rotation='vertical')


# setting up list/array to store timestamps , channel list as input , stimulus conditions
totTimeStampsList = []
userIPchannels = ["A-001","A-002","A-003","A-004"]
tot_stim_condition = ['a','b','c','d']
stimulusComp_Inp = True
no_of_trials = 4
SPKcount_Etrail = []

stim_trial_array = np.nan * np.ones((2000,stimulus_conditions,len(userIPchannels)))

while stimulusComp_Inp:
    
    # note : trial1 => stim_cond1
    #        trial2 => stim_cond2   etc
    for tr,stim_cond in zip(range(no_of_trials),tot_stim_condition):
        channelDict, spkC = SpikeDataPerTrial(userIPchannels)
        totTimeStampsList.append(channelDict)
        plotSPKvsCHNL(channelDict,tr+1)

        stim_trial_array[rep,stim_cond,:] = spkC        
        mn = np.nanmean(stim_trial_array[rep,stim_cond,:],axis=0)       


        spikeCount = 0
        for tsArr in channelDict.values(): #tsArr : time stamp Array
            spikeCount+=len(tsArr)
        SPKcount_Etrail.append(spikeCount)
        y1 = plotSPKvsSTIM(tot_stim_condition.index(stim_cond)+1,spikeCount,y1)    
        #numpy array - no.of spikes vs stim_cond
        # realtime plot after every trial
        # Lauri : save number of spikes in multi dimensional array

    totTimeStamps = defaultdict(list) # keys : channels , values : [timestamps]

    for eachtrial in (totTimeStampsList): # you can list as many input dicts as you want here
        for key, value in eachtrial.items():
            totTimeStamps[key].extend(value)
    
    '''
    plt.figure(3)
    palette = sns.color_palette("dark:red")
    plt.bar(tot_stim_condition,SPKcount_Etrail,color=palette)
    plt.title("no. of spikes vs Stimulus Condition")
    plt.ylabel("count(SPK)")
    '''

    plt.figure(4)
    palette = sns.color_palette("dark:violet")
    plt.bar(totTimeStamps.keys(),[len(totTimeStamps[key]) for key in totTimeStamps.keys()],color=palette)
    plt.title("no. of spikes vs Channel")
    plt.ylabel("count(SPK)")
   
    user_input = input("Enter 'q' to quit: ")
    if user_input == 'q':
        # fig.savefig('plot.png')
        print(SPKcount_Etrail)
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