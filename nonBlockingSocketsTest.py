import logging
import socket
import select

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)

#Blocking socket
def create_blocking(host,ip):
    logging.info('Blocking - creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    logging.info('Blocking - connecting')
    s.connect((host,ip))

    logging.info('Blocking - connected')
    logging.info('Blocking - sending...')
    s.send(b'hello\r\n')

    logging.info('Blocking - waiting...')
    data = s.recv(1024)
    logging.info(f'Blocking - data= {len(data)}')
    logging.info('Blocking - closing...')
    s.close()

#Non Blocking socket 
def create_nonblocking():
    logging.info('Non Blocking - creating socket')
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    logging.info('Non Blocking - connecting')
    s1.bind(('172.27.85.52', 51009)) #BLOCKING
    s1.listen(1)
    '''if ret != 0:
        logging.info('Non Blocking - failed to connect!')
        return'''
    s1.accept()
    logging.info('Non Blocking - connected!')
    s1.setblocking(False)

    inputs = [s1]
    outputs = [s1]
    while inputs:
        logging.info('Non Blocking - waiting...')
        readable,writable,exceptional = select.select(inputs,outputs,inputs,0.5)

        for s1 in readable:
            logging.info(f'Non Blocking - reading...')
            data = s1.recv(1024)
            logging.info(f'Non Blocking - data: {len(data)}')
            logging.info(f'Non Blocking - closing...')
            s1.close()
            inputs.remove(s1)
            break




 
def main():

    create_nonblocking()

if __name__ == "__main__":
    main()