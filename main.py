import socket
import sys
import _thread


clients = []

run = True


def client_handler(conn, addr):
    try:
        global run
        while True:
            msg = conn.recv(2048).decode()
            if msg == '\n' or msg == 'q':
                index = clients.index([x for x in clients if x[1][1] == addr[1]][0])
                del clients[index]
                break
            elif msg == 'admq\n':
                conn.send('adm_end_conn'.encode())
                conn.close()
                run = False
                break
            else:
                if len(clients) == 1:
                    print(f'there\'s only 1 client currently. message was:{msg}')
                else:
                    for dest_sock, dest_addr in clients:
                        if dest_addr[1] == addr[1]:
                            continue
                        else:
                            dest_sock.send(msg.encode())
        conn.close()
    except Exception as err:
        print('bye')


def get_connections(sock):
    while True:
        client, addr = sock.accept()
        print(f'{addr} connected')
        clients.append((client, addr))
        _thread.start_new_thread(client_handler, (client, addr))


def main():
    port = 1512

    sock = socket.socket()
    sock.bind(('localhost', port))
    sock.listen(2)
    _thread.start_new_thread(get_connections, (sock,))
    print('server online')

    while run:
        continue

    sys.exit(0)


if __name__ == '__main__':
    main()
