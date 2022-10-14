inputChannelArray = ["a-001","a-002","a-003","a-004","a-005","a-006",]

tcpCommandSPKchannel = ""

for i in range(len(inputChannelArray)):
    tcpCommandSPKchannel = tcpCommandSPKchannel+"set "+inputChannelArray[i]+".tcpdataoutputenabledspike true;"

print(tcpCommandSPKchannel)

'''
tcpSPKchannel = "set "+channel+".tcpdataoutputenabledspike true"

tcpSPKchannel = tcpSPKchannel.encode("utf-8")
print(tcpSPKchannel) 

spikeDataDict = [{
                    'channel name'  : "a-028",
                    'timestamp'     : "1234"
                },
                {
                    'channel name'  : "a-001",
                    'timestamp'     : "1234"
                },
                {
                    'channel name'  : "a-002",
                    'timestamp'     : "1234"
                },
]
print(spikeDataDict[0]) '''