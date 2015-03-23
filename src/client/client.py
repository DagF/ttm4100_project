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



        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_receiver = MessageReceiver(self,self.connection)

        self.run()
        self.message_receiver.start()

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
            print bcolors.INFO   + bcolors.UNDERLINE  + "Info:\n" + bcolors.ENDC + bcolors.INFO    + payload.get("content") + bcolors.ENDC
        elif response == "message":
            print bcolors.MESSAGE + bcolors.BOLD + timestamp + " " + sender + ":\n"+ bcolors.ENDC + bcolors.MESSAGE + content + bcolors.ENDC

    def send_message(self, data):
        payload = json.dumps(data)
        self.connection.sendall(payload)


    #Handle method functions & dictionary
    def handle_help(self,content):
        self.send_message(self.create_help_message())

    def handle_names(self,content):
        self.send_message(self.create_names_message())

    def handle_logout(self,content):
        self.send_message(self.create_logout_message())

    def handle_login(self, content):
        self.send_message(self.create_login_message(content))

    def handle_msg(self, content):
        self.send_message(self.create_broadcast_message(content))


    handle_options = {
                "handle": handle_help,
                "names": handle_names,
                "logout": handle_logout,
                "login": handle_login,
                "msg": handle_msg
            }


    def handle(self):
        while 42:
            try:
                content = ""
                payload = raw_input()
                if len( payload.split()) > 1:
                    content = payload.split(' ',1)[1]

                request = payload.split()[0]
                print request
                if request in self.handle_options:
                    self.handle_options[request](self, content)
                    if request == "logout":
                        break
                else:
                    print 'not a valid input'
            except KeyboardInterrupt:
                self.send_message(self.create_logout_message())
                break





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
    client = Client('localhost', 2002)
