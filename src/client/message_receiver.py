# -*- coding: utf-8 -*-
from threading import Thread
import time
import json

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and permits
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        super(MessageReceiver, self).__init__()
        self.connection = connection
        self.client = client
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.setDaemon(True)

    def run(self):
        while True:
            payload = self.connection.recv(4096).strip()
            payload_dict = json.loads(payload)
            self.client.receive_message(payload_dict)



