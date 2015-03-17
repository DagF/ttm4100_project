# -*- coding: utf-8 -*-
import socket
import json
import time

from message_receiver import MessageReceiver

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

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_receiver = MessageReceiver(self,self.connection)
        self.run()
        self.message_receiver.start()

        self.handle_login()


        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, payload):
        if payload.has_key("response"):
            response = payload.get("response")
            if response == "error":
                pass
            elif response == "info":
                print("info" + payload.get("content"))
            elif response == "history":
                pass
            elif response == "message":
                pass

    def send_payload(self, data):
        payload = json.dumps(data)
        self.connection.sendall(payload)


    def handle_login(self):
        while self.username == "":
            tmp_username = raw_input("Enter username: ")
            request_dict = { "request": "login",
                             "content": tmp_username}
            self.send_payload(request_dict)
            time.sleep(0.2)

    def login(self, username):
        pass

    def logout(self):
        pass


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 2048)
