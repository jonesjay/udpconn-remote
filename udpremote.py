import socket, argparse, sys, random
MAX_BYTES= 65535
def server(interface, port):
    sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address= sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print('Prentending to drop packets from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('Client at {} says {!r}'.format(address,text))
        message= 'Your data is {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)

def client(hostname, port):
    sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname= sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    delay= 0.1  # seconds
    text = 'This is another message'
    data= text.encode('ascii')
    while True:
        sock.send(data)
        print('Waiting for {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data= sock.recv(MAX_BYTES)
        except:
            delay *= 2 # wait for longer time
            if delay > 7.0:
                raise RuntimeError('Server is down')
        else:   
            break   #we are done, can stop looping 
    print('The server says {!r}'.format(data.decode('ascii')))   

if __name__ == '__main__':
    choices= {'client':client, 'server':server}
    parser= argparse.ArgumentParser(description=('Send and receive udp packets,'
                                                    'packets pretending to be dropped'))
    parser.add_argument('role', choices=choices, help= 'which role to take')
    parser.add_argument('host', help='interface server connects to'
                                        'host client connects to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port(default(1060')
    args= parser.parse_args()
    function= choices[args.role]
    function(args.host, args.p)

    

        
        
       


