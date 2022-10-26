import random

inputList = ['0','1','2','3','4','5']

def shuffle_input(output):
    random.shuffle(output)
    print(output)

shuffle_input(inputList)