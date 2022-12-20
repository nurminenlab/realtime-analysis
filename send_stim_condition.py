import socket
def stimulus_data():
    tot_stim_condition = ['a','c','b','d','e','a','d','c','b','e']
                          #'d','e','b','c','a','e','a','c','d','b',
                          #'d','e','b','c','a','e','a','c','d','b',
                          #'a','c','b','d','e','a','d','c','b','e']'''
    #tot_stim_condition = ['a','c']

    return tot_stim_condition

    #tot_stim_condition = ['a','c','b','d','e','a','d','c','b','e','d','e','b','c','a','e','a','c','d','b']
    #tot_stim_condition = ['a','c','b','c','a','b']
    #tot_stim_condition = ['a','e','c','b','d','c','d','a','b','e']
def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input
    
    while message.lower().strip() != 'end':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()