# -*- coding: utf-8 -*-
import SocketServer
from client_handler import ClientHandler


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):


    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True
    active_clients = {}
    history = []

    def login(self, username, client_handler):
        if username in self.active_clients:
            return False
        else:
            self.active_clients[username] = client_handler
            return True

    def get_history(self):
        return self.history

    def get_active_clients(self):
        return self.active_clients

    def broadcast(self, message):
        self.history.append(message)

        for client in self.active_clients:
            client.send_message(message)

    def logout(self, client_handler):
        self.active_clients.pop(client_handler.get_user_name(), None)




if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 2000
    print 'server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()


