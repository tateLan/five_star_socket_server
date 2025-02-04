import socket
import sys
import _thread
import time


clients = []

run = True

buffer_file = None


def client_handler(conn, addr):
    try:
        global run, buffer_file
        while True:
            msg = conn.recv(2048).decode()
            if msg == '' or msg == 'q':
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
                    buffer_file = open('buffer', 'a+')
                    buffer_file.write(msg)
                    buffer_file.close()
                else:
                    for dest_sock, dest_addr in clients:
                        if dest_addr[1] == addr[1]:
                            continue
                        else:
                            dest_sock.send(msg.encode())
        conn.close()
    except Exception as err:
        print('client disconnected')
        index = clients.index([x for x in clients if x[1][1] == addr[1]][0])
        del clients[index]
        sys.exit(0)


def get_connections(sock):
    global buffer_file
    while True:
        client, addr = sock.accept()
        print(f'{addr} connected')
        clients.append((client, addr))

        buffer_file = open('buffer', 'r+')
        lines = buffer_file.readlines()

        if lines.__len__() > 0:
            for line in lines:
                client.send(line.encode())

        buffer_file.truncate(0)
        buffer_file.close()
        _thread.start_new_thread(client_handler, (client, addr))


def main():
    port = 1512

    sock = socket.socket()
    sock.bind(('localhost', port))
    sock.listen()
    _thread.start_new_thread(get_connections, (sock,))
    print('server online')

    while run:
        time.sleep(3)
        continue

    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as kbi:
        print('buy')
        sys.exit(0)
