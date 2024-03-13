
"""

The main class for collecting, storing, issuing user data. 
It is contained in the list of the Server class and is called to work with the account.

"""


class User:

    def __init__(self, pid, name, rank, status, socket, uid):
        self.pid = pid # Permanent personal ID
        self._name = name
        self._uid = uid # Unique ID for one session
        self._rank = rank # Overall rank for the database
        self._status = status # Database account status: ACTIVE/BANNED
        self._socket = socket
        self._token = "" # Chat token - unique code for one chat
        self._chat_id = 0 # chat id for the current session

    def get_token(self):
        return self._token

    def get_chat_id(self):
        return self._chat_id

    def get_name(self):
    	return self._name

    def get_rank(self):
    	return self._rank

    def set_rank(self, new_rank):
        self._rank = new_rank

    def get_status(self):
    	return self._status

    def set_status(self, status):
        self._status = status
        return True

    def get_socket(self):
        return self._socket

    def get_uid(self):
        return self._uid

    def get_pid(self):
        return self._pid

    def set_token(self, new_token):
        self._token = new_token
        return True

    def set_chat_id(self, new_chat_id):
        self._chat_id = new_chat_id
        return True

    def send(self, message): # send data
        self.get_socket().send(f"{message}".encode("utf-8"))

    def recv(self): # get data
        return self.get_socket().recv(2048).decode("utf-8")


