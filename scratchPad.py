from asyncio.windows_events import NULL


inputChannelArray = ["a-001","a-002","a-003","a-004","a-005","a-006",]

tcpCommandSPKchannel = ""
channelSpikeDict = []
for i in range(len(inputChannelArray)):
    tcpCommandSPKchannel = tcpCommandSPKchannel+"set "+inputChannelArray[i]+".tcpdataoutputenabledspike true;"
    
    #channelSpikeDict[i].channelName = inputChannelArray[i]
    channelSpikeDict.append({
                            'channelName': str(inputChannelArray[i]),
                            'timestamp'  : NULL
                            })

print(f'TCP command is {tcpCommandSPKchannel}\n')

print(f'channel SPK dict {channelSpikeDict}\n')

'''
tcpSPKchannel = "set "+channel+".tcpdataoutputenabledspike true"

tcpSPKchannel = tcpSPKchannel.encode("utf-8")
print(tcpSPKchannel) '''


channelSpikeDict = [{
                    'channelName'  : "a-028",
                    'timestamp'     : "1234"
                },
                {
                    'channelName'  : "a-001",
                    'timestamp'     : "1234"
                },
                {
                    'channelName'  : "a-002",
                    'timestamp'     : "1234"
                },
]
print(channelSpikeDict[0])

samparray =[]
samparray.append({'channelName':"x"})
print(samparray)

inputChannelArray = ["a-001","a-002","a-003","a-004","a-005","a-006"]
d = {channel:[] for channel in inputChannelArray}
print(d)

c = "a-001"


d[c].append(1234)

print(f'after appending {d}')     

channelDict = {'A-000': [13285], 'A-001': [5623], 'A-002': [11353, 12369, 14431, 17471]}
print(channelDict['A-000'])
arr = [ x if x in channelDict['A-002']  else NULL for x in range(20000) ]

import matplotlib.pyplot as plt
plt.scatter(channelDict['A-002'], [ "1" if x in channelDict['A-002'] else NULL for x in range(len(channelDict['A-002'])) ],marker="|")

plt.title('Spike Data')
plt.xlabel('Time (ms)')
plt.xlim((0,20000))
plt.show()

