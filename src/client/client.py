# -*- coding: utf-8 -*-
import socket
import json
import time

from message_receiver import MessageReceiver


class bcolors:
    MESSAGE = '\033[94m'
    INFO = '\033[93m'
    LOGIN = '\033[92m'
    ERROR = '\033[91m'
    HISTORY = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Client:
    """
    This is the chat client class
    """



    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        """
        This method is run when creating a new client object
        """

        self.username = ""
        self.is_logged_in = False
        self.is_logging_out = False

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_receiver = MessageReceiver(self,self.connection)

        self.run()
        self.message_receiver.start()


        print "Welcome to the chatroom!"
        self.send_message(self.create_help_message())
        self.handle()


    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        self.connection.shutdown(socket.SHUT_RDWR)

    def receive_message(self, payload):
        sender = payload.get("sender")
        response = payload.get("response")
        content = payload.get("content")
        timestamp = payload.get("timestamp")

        if response == "error":
            print bcolors.ERROR + content + bcolors.ENDC

        elif response == "info":
            if self.is_logged_in == False:
                if content == "logged in":
                    self.is_logged_in = True
                    print bcolors.LOGIN + "Logged in as: " + self.username + bcolors.ENDC
            if self.is_logging_out == True:
                self.disconnect()
            else:
                print bcolors.INFO   + bcolors.UNDERLINE  + "Info:\n" + bcolors.ENDC + bcolors.INFO    + payload.get("content") + bcolors.ENDC
        elif response == "message":
            print bcolors.MESSAGE + bcolors.BOLD + timestamp + " " + sender + ":\n"+ bcolors.ENDC + bcolors.MESSAGE + content + bcolors.ENDC

    def send_message(self, data):
        payload = json.dumps(data)
        self.connection.sendall(payload)


    def handle_login(self):
        while self.is_logged_in == False:
            self.send_message(self.create_login_message(self.username))
            time.sleep(0.2)

    def handle(self):
        while 42:
            payload = raw_input(self.username + ": ")
            request = payload.split()[0]
            if request == "help":
                self.send_message(self.create_help_message())
            elif request == "names" and self.is_logged_in==True:
                self.send_message(self.create_names_message())
            elif request == "logout" and self.is_logged_in==True:
                self.send_message(self.create_logout_message())
                self.is_logging_out = True
                self.message_receiver.set_is_logged_in(False)
                self.disconnect()
                print "Disconnected from server."
                break
            elif request == "login" and self.is_logged_in==False:
                self.username=payload.split()[1]
                self.handle_login()
            elif request=="msg" and self.is_logged_in==True:
                self.send_message(self.create_broadcast_message(payload))
            else:
                print "Could not interpret query. Try help."
            time.sleep(0.2)



    def create_broadcast_message(self, message):
        return self.create_message("msg", message)

    def create_names_message(self):
        return self.create_message("names", "")

    def create_help_message(self):
        return self.create_message("help", "")

    def create_login_message(self, username):
        return self.create_message("login", username)

    def create_logout_message(self):
        return self.create_message("logout", "")

    def create_message(self, request, content):
        return { "request": request,
                "content": content}



if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('192.168.1.40', 2001)
