
"""
Class that stores information about the message sent by the user.

"""

class Message:

    def __init__(self, author, time, content):
        self.__author = author
        self.__time = time
        self.__content = content

    def get_author(self):
    	return self.__author

    def get_time(self):
    	return self.__time

    def get_content(self):
    	return self.__content

