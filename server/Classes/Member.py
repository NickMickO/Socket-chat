
"""
This class is required for another {Chat} class to work.
Contains basic attributes: 
- username
- user socket
- the user is the owner
"""



class Member:

	def __init__(self, name, socket, owner = False):
		self._name = name
		self._socket = socket
		self._owner = owner

	def get_name(self):
		return self._name

	def get_socket(self):
		return self._socket

	def get_owner(self):
		return self._owner
