# -*- coding: utf-8 -*-
import SocketServer
import json
import re
import datetime
import time
import sys

help_text = "Help: \nmsg    send a message to all users, specify by sending: msg content\names    get the names of all users\nlogout    logout from the chat\nlogin    login <username>"


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def is_valid_username(self, value):
        a = re.compile("^([a-zA-Z0-9])*$")
        return a.match(value)

    def login(self, content):
        if self.is_valid_username(content):
            if self.server.login(self, content):
                self.username = content
                self.send_message(self.create_login_message())
                history = self.server.get_history()
                self.active_dict = self.logged_in_dict
                time.sleep(0.1)
                for message in history:
                    self.send_message(message)
                    time.sleep(0.1)

            else:
                self.send_message(self.create_error_message("Error: Username already in use"))
        else:
            self.send_message(self.create_error_message("Error: Invalid username"))

    def logout(self, content):
        if self.username is not "":
            self.server.logout(self)
            self.active_dict = self.logged_out_dict


        else:
            self.send_message(self.create_error_message("Error: User not logged in"))

    def msg(self, content):
        self.server.broadcast(self.create_broadcast_message(content))

    def names(self, content):
        self.send_message(self.create_names_message())

    def help(self, content):
        self.send_message(self.create_help_message())

    logged_out_dict = {'login': login, 'help': help}
    logged_in_dict = {'logout': logout, 'msg': msg, 'names': names, 'help': help}
    active_dict = logged_out_dict

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ""
        
        #self.send_message(self.create_info_message("Welcome"))

        self.send_message(self.create_help_message())

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            try:
                payload = json.loads(received_string)
                request = payload.get("request")
                content = payload.get("content")

                if request in self.active_dict:
                    self.active_dict[request](self, content)
                else:
                    self.send_message(self.create_error_message("Error: Unknown query"))
            except:
                print(sys.exc_info())
                self.send_message(self.create_error_message("Error: Invalid payload"))



    'Different messages to be sent:'
    def create_login_message(self):
        return self.create_message(self.get_time_stamp(), "server", "info", "logged in")

    def create_logout_message(self):
        return self.create_message(self.get_time_stamp(), "server","info","logged out")

    def create_error_message(self, error):
        return self.create_message(self.get_time_stamp(), "server","error",error)

    def create_broadcast_message(self,content):
        return self.create_message(self.get_time_stamp(), self.username,"message",content)

    def create_help_message(self):
        return self.create_message(self.get_time_stamp(), "Server","info",help_text)

    def create_info_message(self, message):
        return self.create_message(self.get_time_stamp(), "Server","info",message)


    def create_names_message(self):
        names_string = self.server.get_active_clients_names()
        return self.create_message(self.get_time_stamp(), "server","info", names_string)


    'Other methods:'
    def send_message(self, data):
        payload = json.dumps(data)
        self.connection.sendall(payload)

    def create_message(self, timeStamp, sender, response, content):
        return {"timestamp": timeStamp,
        "sender": sender,
        "response": response,
        "content": content}

    def get_time_stamp(self):
        str_time = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S")
        return str_time



    def get_user_name(self):
        return self.username


