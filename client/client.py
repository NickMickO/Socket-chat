import socket
from threading import Thread


class Client():

    def __init__(self):
        self.ip = "121.0.0.1"
        self.port = 8001
        self.socket = client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, )

    def set_up(self):
        try:
            with open("client_settings.txt", "r") as config:
                l1 = config.readline()
                l2 = config.readline().split()
                self.ip = l2[1]
                self.port = int(l2[2])
        except FileNotFoundError:
                print ("[ERROR] : Config not found!")
                with open("client_settings.txt", "w") as config:
                    config.write(f"# Client options \nhost: 127.0.0.1 8001") 
                self.ip = "127.0.0.1"
                self.port = 8001
        while True:
            try:
                id = self.ip
                self.socket.connect(
                        (id, self.port) # bind hosting port and adress
                )
                break
            except Exception as error:
                print (f"[ERROR] : {error}")

        self.main()


    def listen(self):
        try:
            data = self.socket.recv(2048)
            while True:
                data = self.socket.recv(2048)
                print (data.decode("utf-8"))
        except Exception as error:
            print (f"[Error] : {error}")

    def main(self):
        print ("\n \n \n \n|      Connected to the server!          |")
        listen_thr = Thread(target=self.listen)
        listen_thr.start()
        try:
            self.socket.send("0".encode("utf-8"))
            while True:
                self.socket.send(input("").encode("utf-8"))
        except Exception as error:
            print (f"[Error] : {error}")
            input()
            return

client = Client()
client.set_up()