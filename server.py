################################
#*Name: Matthew Toutounjian
#*Date: 2/11/18
#*Objective: GIT Alternative for
#version Control (server)
################################

import socket
import random
import time
import threading
import os
import sys
import hashlib

#global definitions start here
AUTH_FILE = "authentication.txt"
HOST = ""
PORT = 8000
MAX_CLIENTS = 500
LOCK = threading.Lock()
BUFF_SIZE = 16777216
#global definitions end here

class Server:
    def __init__(self):
        print("[INFO] Starting server... -_-")
        self.clients = []
        self.messages = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        threading.Thread(target=self.listener).start()
    def listener(self):
        for x in range(MAX_CLIENTS):
            self.sock.listen()
            self.conn, self.addr = self.sock.accept()
            self.clients.append(self.conn)
            threading.Thread(target=self.recver, args=(self.conn,)).start()
            with LOCK:
                print("[INFO] {} has successfully connected!".format(self.addr))
    def CredentialsAreValid(self, uid, pw):
        uid_correct = False
        pw_correct = False
        f = open(AUTH_FILE, "r")
        for line in f:
            user_id, password = line.split(":")
            if user_id == uid:
                uid_correct = True
            if password == pw:
                pw_correct = True
        f.close()
        if pw_correct == True and uid_correct == True:
            return True
        else:
            return False
    def recver(self, conn):
        self.uid = conn.recv(BUFF_SIZE).decode("utf-8")
        self.pw = conn.recv(BUFF_SIZE)
        hasher = hashlib.sha256()
        hasher.update(self.pw)
        self.hashed_pw = hasher.hexdigest()
        if self.CredentialsAreValid(self.uid, self.hashed_pw):
            conn.send("Successfully Logged In!".encode("utf-8"))
            while True:
                self.msg_recved = conn.recv(BUFF_SIZE).decode("utf-8")
                self.messages.append(self.msg_recved)
                if self.msg_recved[:4] == "push":
                    fname = self.msg_recved[5:]
                    self.file = conn.recv(BUFF_SIZE).decode("utf-8")
                    with open(fname, "w") as fp:
                        fp.write(self.file)
                        fp.close()
                    conn.send("[INFO] File Received! :)".encode("utf-8"))
                elif self.msg_recved[:4] == "pull":
                    fname = self.msg_recved[4:]
                    with open(fname, "r") as fp:
                        self.file_contents = fp.read()
                        conn.send(self.file_contents.encode("utf-8"))
                    time.sleep(.1)
                    conn.send("[INFO] File Sent!".encode("utf-8"))
                elif self.msg_recved == "show":
                    dir_path = os.path.dirname(sys.argv[0])
                    files = os.listdir(dir_path)
                    msg = '\n'.join(files)
                    conn.send(msg.encode("utf-8"))
        else:
            conn.send("Credentials are not valid!".encode("utf-8"))

def main():
    server = Server()

if __name__ == "__main__":
    main()
