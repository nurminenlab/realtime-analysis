import threading

def printit():
    t = threading.Timer
    #t.daemon = True
    t(2.0, printit).start()
    print ("Hello, World!")

printit()