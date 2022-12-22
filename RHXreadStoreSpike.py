from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
import time, socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from ctypes import sizeof
import statistics
from tkinter import *
import seaborn as sns
import numpy as np
from collections import defaultdict
import random
from statistics import mean
from send_stim_condition import stimulus_data
from numba import njit,cuda
import pandas as pd
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

  
def ReadSpikeDataPerTrial(inputChannelArray,stim_cond):

    channelDict = {channel:[] for channel in inputChannelArray}

    # run for 600ms - 0.6s - to read the data
    time.sleep(0.6) 

    rawData = sSPK.recv(200000)
    #print(rawData)

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

    for block in range(numBlocks): # loops through every SPIKE from all streamed channels
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

        stim_SPK_Count[stim_cond] = spikeCount

    for ch in channelDict:
        data_df.loc[len(data_df)] = [ch,stim_cond,len(channelDict[ch])] # CHECK time(append) VS time(loc)

    # get trial here => (1 stim_cond, n channels)

    for ch,ax in zip(userIPchannels,axes3):
        ax.cla()
        MEAN = data_df[data_df['Channel']==ch].groupby('stim_cond')['SPK_count'].mean()
        SEM = data_df[data_df['Channel']==ch].groupby('stim_cond')['SPK_count'].sem()
        ax.errorbar(x = MEAN.index, # stimulus conditions
                    y = MEAN, 
                    yerr= SEM,
                    label=ch,capsize=2,fmt ='o')
        ax.legend()        
        

    return channelDict,stim_SPK_Count


def plotSPKvsSTIM(stim_cond,SPKcount,n): #x = stim_cond  y = SPKcount (int)
    
    if stim_cond not in plotSPKvsSTIM_xy.keys():
        plotSPKvsSTIM_xy[stim_cond] = [SPKcount]    
    else:
        plotSPKvsSTIM_xy[stim_cond].append(SPKcount) #= [plotSPKvsSTIM_xy[stim_cond],SPKcount]
    n += 1
    x1 = list(plotSPKvsSTIM_xy.keys())
    y1 = list(mean(plotSPKvsSTIM_xy[key]) for key in plotSPKvsSTIM_xy.keys())
    yerr = list((statistics.pstdev(plotSPKvsSTIM_xy[key])/math.sqrt(n)) for key in plotSPKvsSTIM_xy.keys())
    ax.cla()
    ax.errorbar(x1,y1,yerr=yerr,capsize=2,fmt ='o')

    fig2.canvas.draw()
    fig2.canvas.flush_events()
    time.sleep(0.0002)
    return n

def setup_TCPconnection():    
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

if __name__ == '__main__':
    
    # get input channels from user
    channel_window = Tk()    
    channels = ["A-000","A-001","A-002","A-003","A-004","A-005","A-006","A-007","A-008","A-009","A-010"]
    userIPchannels=[]
    for x in range(len(channels)):
        l = Checkbutton(channel_window, text=channels[x], variable=channels[x],command=lambda x=channels[x]:userIPchannels.append(x))
        l.pack(anchor = 'w')
    Button(channel_window,text="Ok",command=lambda: [print("selected channels ",userIPchannels),channel_window.destroy()]).pack()
    channel_window.mainloop()
            
    if len(userIPchannels) > 10 or len(userIPchannels) < 1:
        raise Exception("Check the number of input channels \n min :2 & max :10 ")

    if stimulus_data():
        stimulusComp_Inp = True
        
    else:
        stimulusComp_Inp = False

    # number of elements in the sample
    n = 0
    
    
    # setting up plot 
    print("opening plot......")
    plt.ion() # Enable interactive mode for plot


    #plot setup for number of spikes and stim_conditions
    x1 = [str()]
    #y1 = np.array([None])  initializing an empty numpy array
    y1 =[int()] # initialzing with None since x1 is initialized with empty string list
    fig2, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0,6) #xlim = unique_stim_conditions++
    ax.set_ylim(0,50)
    fig2.suptitle('No. of SPK vs Stimulus conditions')
    fig2.text(0.5, 0.04, 'Stimulus conditions', ha='center', va='center')
    fig2.text(0.06, 0.5, 'count(SPK)', ha='center', va='center', rotation='vertical')
    #ax.set_xticklabels(['a','b','c','d','e','f'])
 
    # setting up list/array to store timestamps , channel list as input , stimulus conditions
    totTimeStampsList = []
    plotSPKvsSTIM_xy = {}
    stim_SPK_Count = {}

    #print('Stimulus Condition Data ',stimulus_data())
    data_df = pd.DataFrame(columns=['Channel','stim_cond','SPK_count'])

    fig3,axes3 = plt.subplots(nrows=3,ncols=4,figsize=(10, 10))
    axes3  = np.reshape(axes3,(12,))
    fig3.suptitle('channels X SPKcounts')




    if stimulusComp_Inp:
        setup_TCPconnection()
        unique_count_stim_condn = len(list(set(stimulus_data()))) # 5 => unique(tot_Stim_condition)
        runs = len(stimulus_data())
        data = np.empty((0,unique_count_stim_condn))
        for i in range(len(userIPchannels)):
            tcpCommandSPKchannel ="set "+userIPchannels[i]+".tcpdataoutputenabledspike true;" 
            tcpCommandSPKchannel = tcpCommandSPKchannel.encode("utf-8")
            scommand.sendall(tcpCommandSPKchannel)

        scommand.sendall(b'set runmode run')
        # note : trial1 => stim_cond1 for n channels
        #        trial2 => stim_cond2 for n channels  etc

        for run,stim_cond in zip(range(1,runs+1),stimulus_data()):

            channelDict,stim_SPK_Count = ReadSpikeDataPerTrial(userIPchannels,stim_cond)

            if (run)%unique_count_stim_condn == 0: # every repetition
                data = np.append(data,np.array([list(stim_SPK_Count.values())]),axis = 0)
    
            totTimeStampsList.append(channelDict)
            spikeCount = 0
            for tsArr in channelDict.values(): #tsArr : time stamp Array
                spikeCount+=len(tsArr)            

            n = plotSPKvsSTIM(stim_cond,spikeCount,n)
        scommand.sendall(b'set runmode stop')  
        totTimeStamps = defaultdict(list) # keys : channels , values : [timestamps]

        for eachtrial in (totTimeStampsList): # you can list as many input dicts as you want here
            for key, value in eachtrial.items():
                totTimeStamps[key].extend(value)


        


        #plot No. of SPK vs Stimulus conditions

        stimulus_cond = [data[:,i] for i in range(len(data[0]))]
        fig4, axes4 = plt.subplots()
        fig4.suptitle('No. of SPK vs Stimulus conditions')
        axes4.boxplot(stimulus_cond,showmeans=True)

        # plot No. of spikes vs Channel
        plt.figure(5)
        palette = sns.color_palette("dark:violet")
        plt.bar(totTimeStamps.keys(),[len(totTimeStamps[key]) for key in totTimeStamps.keys()],color=palette)
        plt.title("No. of spikes vs Channel")
        plt.ylabel("count(SPK)")

              
        user_input = input("Enter 'q' to quit: ")

        if user_input == 'q':
            '''print(data) # spk & stim cond
            print(data_df) # spk & channel
            print("n is ", n )'''
            data_df.to_csv('CH_stim_SPK_data.csv')
            


    else:
        scommand.sendall(b'set runmode stop')
        raise Exception("No Stimulus Input Present, intan TCP connection terminated")
        









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

