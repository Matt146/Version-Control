import socket
import random
import time
import threading
import sys
import os

#global definitions start here
HOST = "localhost"
PORT = 8000
LOCK = threading.Lock()
BUFF_SIZE = 16777216
#global definitions end here

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = []
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            print(e)
        self.login()
        self.response = self.sock.recv(BUFF_SIZE).decode("utf-8")
        if self.response == "Credentials are not valid!":
            print("Invalid Credentials! :'(")
            quit()
        self.PrintOptions()
        choice = int(input("@> "))
        if choice == 1:
            dir = str(input("Enter folder directory: "))
            print("Sending files!")
            files = os.listdir(dir)
            for file in files:
                self.push(file)
            print("Sent files!")
        elif choice == 2:
            self.show()
            file_chosen = str(input("Which file would you like: "))
            packet = str("pull" + file_chosen).encode("utf-8")
            self.sock.send(packet)
            file_data = self.sock.recv(BUFF_SIZE).decode("utf-8")
            f = open(file_chosen, "w")
            f.write(file_data)
            f.close()
    def login(self):
        self.uid = str(input("Enter user user ID: "))
        self.pw = str(input("Enter your password: "))
        self.sock.send(self.uid.encode("utf-8"))
        self.sock.send(self.pw.encode("utf-8"))
    def PrintOptions(self):
        print("------------------")
        print("(1) Upload Folder")
        print("(2) Receive Files")
        print("------------------")
    def push(self, fname):
        print("Sending files...")
        t1 = time.time()
        with open(fname, "r") as fp:
            self.file_contents  = fp.read()
            self.sock.send(str("push " + str(fname)).encode("utf-8"))
            time.sleep(.1)
            self.sock.send(str(self.file_contents).encode("utf-8"))
        t2 = time.time()
        print("Files sent! | Time taken: {}".format(t2-t1))
        server_response = self.sock.recv(BUFF_SIZE).decode("utf-8")
        print("Server response: {}".format(server_response))
    def pull(self, fname):
        print("Getting files...")
        t1 = time.time()
        with open(fname, "w") as fp:
            self.sock.send(str("pull" + fname).encode("utf-8"))
            time.sleep(.1)
            self.file_contents_recved = self.sock.recv(BUFF_SIZE).decode("utf-8")
            fp.write(self.file_contents_recved)
        t2 = time.time()
        server_response = self.sock.recv(BUFF_SIZE).decode("utf-8")
        print("Server response: {}".format(server_response))
        print("Files received | Time taken: {}".format(t2-t1))
    def show(self):
        self.sock.send("show".encode("utf-8"))
        server_response = self.sock.recv(BUFF_SIZE).decode("utf-8")
        print("Server response: {}".format(server_response))

if __name__ == "__main__":
    client = Client()
