import socket, select, sys, string, threading

CLIENTS = {} # contains my server socket and everyone's client socket (5 sockets)
RECV_BUFFER = 4096
PORT = 5001

HOST = ["172.22.146.231", "172.22.146.233", "172.22.146.235", "172.22.146.237", "172.22.146.239"] # all of the hosts allowed in this group chat
SEND_SOCKS = [] # all of my sockets I need to write to other servers (4 sockets)

GET_SOCKET = socket.socket
AF_INET = socket.AF_INET
SOCK_STREAM = socket.SOCK_STREAM

# handles new connections and messages from other clients
def handleNewConnections():
    server_socket = GET_SOCKET(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    CLIENTS[server_socket] = 'SERVER'

    print "Chat server started on port " + str(PORT)

    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CLIENTS.keys(),[],[])
        for sock in read_sockets:
            # new connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CLIENTS[sockfd] = ''
            else: # message from another client
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        if data[0:4] == "?!@#":
                            CLIENTS[sock] = data[4:]
                            print CLIENTS[sock] + " connected"
                            # broadcast_data(sockfd,"\r" + CLIENTS[sock] + " entered room\n")
                            print "\r" + CLIENTS[sock] + " entered room"
                        else:
                            print "\r" + "<" + CLIENTS[sock] + '> ' + data
                            # broadcast_data(sock, "\r" + '<' + CLIENTS[sock] + '> ' + data)
                except:
                    s = sock

def prompt():
    sys.stdout.write('<' + username + '> ')
    sys.stdout.flush()

def send_message(msg):
    for s in SEND_SOCKS:
        try:
            s.send(msg)
        except:
            s = socket

if __name__=="__main__":
    if(len(sys.argv) != 2):
        print 'Usage : python distributed_group_chat.py username'
        sys.exit()

    username = sys.argv[1]

    thread = threading.Thread(target = handleNewConnections)
    thread.start()
    print socket.gethostname()
    HOST.remove(socket.gethostbyname(socket.gethostname())) 
    while 1:
        for host in HOST:
            s = GET_SOCKET(AF_INET, SOCK_STREAM)
            try:
                s.connect((host, PORT))
                SEND_SOCKS.append(s)
                HOST.remove(host)
                s.send("?!@#" + username)
            except:
                socket = s
                # do nothing
        prompt()
   
        read_sockets, write_sockets, error_sockets = select.select([sys.stdin], [], [])
        for sock in read_sockets:
            if sock == sys.stdin:
                msg = sys.stdin.readline()
                send_message(msg)

    thread.join()


'''
def broadcast_data (sock, message):
    for socket in CLIENTS.keys():
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                if socket in CLIENTS:
                    socket.close()
                    del CLIENTS[socket]

'''