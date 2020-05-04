import socket
import _thread


clients = []


def client_handler(conn, addr):
    while True:
        msg = conn.recv(2048).decode()
        if msg == '' or msg == 'q':
            index = clients.index([x for x in clients if x[1][1] == addr[1]][0])
            del clients[index]
            break
        else:
            if len(clients) == 1:
                print(f'there\'s only 1 client currently. message was:{msg}')
            else:
                print(msg)
                for dest_sock, dest_addr in clients:
                    if dest_addr[1] == addr[1]:
                        continue
                    else:
                        dest_sock.send(msg.encode())
    conn.close()


def main():
    port = 1512

    sock = socket.socket()
    sock.bind(('localhost', port))
    sock.listen(2)

    print('server online')

    while True:
        client, addr = sock.accept()
        print(f'{addr} connected')
        clients.append((client, addr))
        _thread.start_new_thread(client_handler, (client, addr))


if __name__ == '__main__':
    main()