from tkinter import *

inputChannelWindow = Tk()
inputChannelWindow.geometry("250x500") 
inputChannelWindow.title("Get Input channels")
ch = ['A','B','C','D','E','F','G','H']
channels = {}
for i in ch :
    channel = Label(inputChannelWindow,text = "channel"+i)
    channel.pack()
    channels[i] = {}
    channels[i] = Entry(inputChannelWindow)
    channels[i].pack(pady=(5,10))
    

def getChannelNames():
    chan = []
    for key in channels:
        c = [key +"-" + n for n in (channels[key].get()).split(',')]
        chan.extend(c)
    return chan

Button(inputChannelWindow,text="Done",command=lambda: [print("selected channels ",getChannelNames()),inputChannelWindow.destroy()]).pack()

inputChannelWindow.mainloop()