from Classes.Message import Message
from Classes.Member import Member


"""
A class that stores information about the chat and a list of participants. 
Uses the Member class.
"""

class Chat:

    def __init__(self, token, owner = 0, owner_socket = 0):
        self._name = f"{owner}'s Chat!"
        self._token = token
        if owner != 0:
            self._members = [Member(owner, owner_socket)]
        else:
            self._members = []
        self._banned_members = []
        self._owner = owner
        self._limit = 9 # Max users
        self._messages = []

    def get_token(self):
        return self._token

    def get_owner(self):
        if self._owner != 0:
            return self._owner
        else:
            return False

    def get_banned_members(self):
        return self._banned_members

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        for member in self.get_members():
            member.get_socket().send(f"* Chat name was changed: {new_name}".encode("utf-8"))
        self._name = new_name

    def get_members(self):
        return self._members

    def get_messages(self):
        return self._messages


    def member_join(self, member_name, member_socket):
        for member in self.get_members():
            member.get_socket().send(f"| {member_name} connected!".encode("utf-8"))
        self._members.append(Member(member_name, member_socket))
        return True

    def member_leave(self, member_name):
        counter = 0
        for member in self.get_members():
            member.get_socket().send(f"| {member_name} left!".encode("utf-8"))
            if member.get_name() == member_name:
                self._members.remove(self._members[counter])
                break
            counter += 1
        return True
    
    def find_member(self, member_name):
        for member in self.get_members():
            if member_name == member.get_name():
                return member
        return False

    def kick_member(self, member_name):
        counter = 0
        id = 0
        for member in self.get_members():
            if member.get_name() != member_name:
                member.get_socket().send(f"| {member_name} was kicked! |".encode("utf-8"))
                counter += 1
            else:
                id = counter
        self.get_members()[id].get_socket().send("| You was kicked from lobby by owner! |".encode("utf-8"))
        self._members.remove(self._members[id])
        return True

    def ban_member(self, member):
        if member in self.get_members():
            member.get_socket().send("| You was banned by owner! |".encode("utf-8"))
            self._banned_members.append(member.get_name())
            self._members.remove(member)
            return True

    def unban_member(self, member_name):
        if member_name in self._banned_members:
            self._banned_members.remove(member_name)
            return True

    def new_message(self, message, author, rmg=True):
        self._messages.append(Message(author, 0, message))
        mg = self._messages[len(self._messages) - 1] # message
        if rmg == True:
            return mg
        else: # rmg = False
            return True


    def members_list(self, USER):
        USER.send("* Members: ")
        for member in self.get_members():
            USER.send(f"{member.get_name()} \n")

        




