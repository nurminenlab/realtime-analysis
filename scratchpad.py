from asyncio.windows_events import NULL


import matplotlib as plt

channelDict = {'A-000': [609], 'A-001': [5290], 'A-002': [9371], 'A-003': [6029, 7665, 8055, 8465, 10763, 14605, 15243, 18067, 18382]}


print([ None if x in channelDict['A-000'] else 1 for x in range(len(channelDict['A-000'])) ])

