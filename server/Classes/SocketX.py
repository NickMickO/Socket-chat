import socket

"""
Binds and commands

"""

class SocketX:

    @staticmethod
    def create_socket():
        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            )
        return server

    @staticmethod
    def bind(server, id, port): # address and port
        server.bind(
            (id, port) 
            )

    @staticmethod
    def setListen(server, x):
        server.listen(x)

    @staticmethod
    def connect(server):
        user_socket, address = server.accept()
        return user_socket, address

    @staticmethod
    def close(server):
        server.close()