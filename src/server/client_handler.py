# -*- coding: utf-8 -*-
import SocketServer
import json
import re
import datetime
import time

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ""

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            print(received_string)
            payload = json.loads(received_string)

            if self.is_valid_payload( payload ):
                request = payload.get("request")
                content = payload.get("content")
                if request == "login":
                    if self.server.login(content, self):
                        self.username = content

                        self.send_message({"timestamp": datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S"),
                                           "sender": "Server",
                                           "response": "info",
                                            "content": self.username
                                        })
                    else:
                        self.send_message({"timestamp": datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y %H:%M:%S"),
                                           "sender": "Server",
                                           "response": "error",
                                            "content": "Username already in use."
                                        })

                elif request == "logout":
                    pass
                elif request == "msg":
                    pass
                elif request == "names":
                    pass
                elif request == "help":
                    pass
                else:
                    #
                    pass
            else:
                print("invalid payload")

    def send_message(self, data):
        payload = json.dumps(data)
        self.connection.sendall(payload)

    def is_valid_payload(self, payload):
        if not payload.has_key("request"):
            print("request key")
            return False
        if not payload.has_key("content"):
            print("request key")
            return False
        if not self.is_valid_value(payload.get("request")):
            print("request value")
            return False
        if not self.is_valid_value(payload.get("content")):
            print("request value")
            return False

        return True

    def is_valid_value(self, value):
        a = re.compile("^([a-zA-Z0-9])*$")
        return a.match(value)

