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