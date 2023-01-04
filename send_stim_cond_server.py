import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5004  # initiate port number above 1024

    server_socket = socket.socket()  # get instance
    # The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    print("Ready to send Stimulus Conditions")
    data = conn.recv(1024).decode()
    if data == 'ready':
        while True and data != 'end':
            # receive data stream. it won't accept data packet greater than 1024 bytes
            if not data:
                # if data is not received break
                break

            data = input(' enter stim condition -> ')
            conn.send(data.encode())  # send data to the client

        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()