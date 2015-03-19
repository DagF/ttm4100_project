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

    def login(self, client_handler, username):
        if username in self.active_clients:
            print "Failed login attempt: " + username
            return False
        else:
            self.active_clients[username] = client_handler
            print "Login: " + username
            return True

    def get_history(self):
        return self.history

    def get_active_clients(self):
        return self.active_clients

    def broadcast(self, message):
        self.history.append(message)

        for key, client in self.active_clients.iteritems():
            client.send_message(message)

    def logout(self, client_handler):
        print(client_handler.get_user_name())
        del self.active_clients[client_handler.get_user_name()]
        print(self.active_clients)




if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 2001
    print 'server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()


