import threading
import time
import random


from Classes.SocketX import SocketX
from Classes.Database import Database
from Classes.Chat import Chat
from Classes.Hasher import Hasher
from Classes.User import User
from Classes.Message import Message
from Classes.Console import Console
from Classes.Command import Command




"""
The main Server class for handling user requests,
creating threads and sending queries to the database.
Also in this class there is a socket binding,
processing input from the console, 
creating Chat and User classes for storing and processing user data.

"""


class Server(SocketX):

    def __init__(self, settings, version, commands_list, ranks_list):
        self.ip = settings["ip"]
        self.port = int(settings["port"])
        self.max_users = int(settings["max_users"])
        self.max_chats = int(settings["max_chats"])
        self.chats = [] # list with chats objects
        self.users = []
        self.users_threads = []
        self.version = version
        self.token_len = int(settings["token_len"])
        self.global_chat = bool(settings["global_chat"])
        self.username_len = int(settings["username_len"])
        self.userpass_len = int(settings["userpass_len"])
        self.minadmin_rank = int(settings["minadmin_rank"])
        self.maxadmin_rank = int(settings["maxadmin_rank"])
        self.guests = bool(settings["guests"])
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        self.server = 0
        self.commands = commands_list
        self.active = False
        self.set_up()


    def set_up(self):
        print (f"Version {self.version}")
        print ("[LOG] Create socket...")
        self.server = self.create_socket()
        print ("[LOG] Binding...")
        while True:
            try:
                self.bind(self.server, self.ip, self.port)
                self.setListen(self.server, self.max_users)
                break
            except Exception as error:
                print (f"[ERROR] {error}")
                print ("Reset ip and port? y/n")
                if str(input) == "y":
                    self.ip = "127.0.0.1"
                    self.port = 8001

        self.active = True
        self.main()



    def main(self):
        consoles = threading.Thread(target=Console.init, args=(self,)) # Create thread for console commands
        consoles.start()

        # Create Global chat:
        if self.global_chat:
            self.chats.append(Chat(1))
            self.chats[0].set_name("GLOBAL CHAT")

        print ("[LOG] Database connected...")
        Database.init()
        self.connect_users()


#   Connect user and create thread
    def connect_users(self):
        while True:
            if self.active:
                user, address = self.connect(self.server)
                user_thread = threading.Thread(target=self.user_thread,  args=(user, address,))
                user_thread.start() # User was connected and User now listening
                self.users_threads.append(user_thread)


    def user_thread(self, user, adr):
        
            while True:
                user.send(f"111.111.111\n".encode("utf-8")) # Send user data(check)
                data = user.recv(2048).decode("utf-8")

                if data == "0":
                    break
                else:
                    user.close() # Close connection and thread
                    return


            # Sign up or sign in 
            buf = self.db_operations(5, self.sign(user, adr))
            if buf != False:
                buf = buf[0]
                user_id = len(self.users)
                USER = User(buf[0], buf[1], buf[3], buf[5], user, user_id)
                self.users.append(USER)
            else:
                user.close()
                return
            
            try:
                # Loop to connect to chat
                Run = False
                while True:
                    ##
                    USER.send("* Write !connect 'token' or !create chat ")
                    data = USER.recv()
                    entry = data.split()

                    if entry[0] == "!create" and entry[1] == "chat":
                            
                            # Create token
                            token = self.generate_new_token()

                            # Create chat object
                            self.chats.append(Chat(token, USER.get_name(), USER.get_socket()))
                            chat_id = len(self.chats) - 1
                            USER.send(f"Chat created. token: {token}")
                            USER.send("| !help to get commands")
                            USER.set_token(token)
                            USER.set_chat_id(chat_id)
                            Run = True
                            print (f"[LOG] CREATED NEW CHAT, ID: {chat_id}")

                    if entry[0] == "!connect":
                            n = 0
                            # Global chat
                            if data == "!connect" and self.global_chat:
                                self.chats[0].member_join(USER.get_name(), USER.get_socket())
                                USER.set_chat_id(0)
                                USER.set_token(1)
                                USER.send("| Connected to GLOBAL CHAT!")
                                Run = True
                            else:
                                # Private chat
                                for chat in self.chats:
                                    if chat.get_token() == entry[1] and USER.get_name() not in chat.get_banned_members():
                                        chat.member_join(USER.get_name(), USER.get_socket())
                                        USER.set_chat_id(n) # n = chat_id
                                        USER.send(f"| Connected to {chat.get_name()}! |")
                                        USER.send(f"* You connected to private chat. Use !leave to leave chat")
                                        Run = True
                                        break

                                    # This condition does not allow a banned user to join
                                    if chat.get_token() == entry[1] and USER.get_name() in self.chats[chat_id].get_banned_members():
                                            USER.send("| You was banned by owner! |")
                                            Run = False
                                            USER.set_chat_id(0)
                                    n += 1


                    master_commands = ["!help", "!get_user", "!ban", "!unban", "!users", "!get_version"]
                    if entry[0] in master_commands:
                        if entry[0] == "!get_version":
                            USER.send(f"* SERVER VERSION: {self.version}")
                        else:
                            self.admin_commands(USER, entry)



                    # Main Loop for Chat Interactions
                    while Run:

                        data = USER.recv()
                        entry = data.split()

                        # Auxiliary condition for the user to be kicked out of the chat
                        in_chat = False
                        for member in self.chats[USER.get_chat_id()].get_members():
                            if member.get_name() == self.users[USER.get_uid()].get_name():
                                in_chat = True
                                break

                        if not in_chat:
                            Run = False
                            chat_id = 0

                        else:

                            mg = self.chats[USER.get_chat_id()].new_message(data, USER.get_name())
                            chat_commands = ["!help", "!kick", "!ban", "!unban", "!members", "!change_name", "!close", "!leave", "!get_chat_name", "!get_owner", "!get_messages"]
                            if entry[0] in chat_commands:
                                self.commands_in_chat(USER, entry, mg)
                            else:

                                # Send new message
                                if len(entry) > 1 and (entry[0] == "!roll" or entry[0] == "!me"):
                                    if entry[0] == "!roll":
                                        try:
                                            roll = random.randint(0, int(entry[1])) 
                                            for member in self.chats[USER.get_chat_id()].get_members():
                                                member.get_socket().send(f"{mg.get_author()} rolls a die for {entry[1]}. Dropped out {roll}".encode("utf-8"))
                                        except ValueError:
                                            print ("[WARN] ValueError in roll command!")
                                    elif entry[0] == "!me":
                                        for member in self.chats[USER.get_chat_id()].get_members():
                                            member.get_socket().send(f"{mg.get_author()} does {entry[1]}".encode("utf-8"))
                                else: 
                                    for member in self.chats[USER.get_chat_id()].get_members():
                                        member.get_socket().send(f"{mg.get_author()} : {mg.get_content()}".encode("utf-8"))
            except Exception as error:
                # Completing the work
                for chat in self.chats:
                    for member in chat.get_members():
                        if member.get_name() == USER.get_name():
                            chat._members.remove(member)
                            break
                try:
                    USER.get_socket().close()
                except:
                    pass
                for u in self.users:
                    if u == USER:
                        self.users.remove(USER)
                        break
                print (f"[ERROR] {error}")



    def commands_in_chat(self, USER, entry, mg):

        if entry[0] == "!help" and mg.get_author() == self.chats[USER.get_chat_id()].get_owner():
            USER.send("* Owner commands ** help \n List with commands: \n !help \n !kick \n !ban \n !unban \n !members \n !change_name \n !close \n !leave \n !roll (0-'X') \n !get_chat_name \n !get_owner \n !me \n !get_messages \n []")           
        elif entry[0] == "!help":
            USER.send("* Member commands ** help \n List with commands: \n !help \n !members \n !leave \n !roll (0-'X') \n !get_chat_name \n !get_owner \n !me \n !get_messages \n []")
        elif entry[0] == "!get_chat_name":
            USER.send(f"* Chat: {self.chats[USER.get_chat_id()].get_name()}")
        elif entry[0] == "!get_owner":
            USER.send(f"* Owner: {self.chats[USER.get_chat_id()].get_owner()}")
        elif entry[0] == "!get_messages":
            for message in self.chats[USER.get_chat_id()].get_messages():
                USER.send(f"{message.get_author()} : {message.get_content()}")
                time.sleep(0.2)
        elif entry[0] == "!kick" and mg.get_author() == self.chats[USER.get_chat_id()].get_owner() and len(entry) >= 2:
            counter = 0
            for member in self.chats[USER.get_chat_id()].get_members():
                if member.get_name() == entry[1]:
                    pass
            else:
                counter += 1
            if counter == len(self.users):
                USER.send(f"* Uncorrect name! This user does not exist!")
            else:
                self.chats[USER.get_chat_id()].kick_member(entry[1])
        elif entry[0] == "!members":
            self.chats[USER.get_chat_id()].members_list(USER)
        elif entry[0] == "!change_name" and mg.get_author() == self.chats[USER.get_chat_id()].get_owner() and len(entry) >= 2:
            self.chats[USER.get_chat_id()].set_name(entry[1])
        elif entry[0] == "!ban" and mg.get_author() == self.chats[USER.get_chat_id()].get_owner() and len(entry) >= 2:
            for member in self.chats[USER.get_chat_id()].get_members():
                if member.get_name() == entry[1]:
                    self.chats[USER.get_chat_id()].ban_member(member)
                member.get_socket().send(f"| {entry[1]} was banned! |".encode("utf-8"))
        elif entry[0] == "!close" and mg.get_author() == self.chats[USER.get_chat_id()].get_owner():
            ban_list = []
            for member in self.chats[USER.get_chat_id()].get_members():
                ban_list.append(member)
            for member in ban_list:
                self.chats[USER.get_chat_id()].ban_member(member)
            # Ban everyone
        elif entry[0] == "!unban" and mg.get_author() ==  self.chats[USER.get_chat_id()].get_owner() and len(entry) >= 2:
            self.chats[USER.get_chat_id()].unban_member(entry[1])
        elif entry[0] == "!leave":
            self.chats[USER.get_chat_id()].member_leave(USER.get_name())
            USER.set_token(0) 
            USER.set_chat_id(0)




    def admin_commands(self, USER, entry):
        if USER.get_rank() > 1:
            if entry[0] == "!help":
                USER.send("* Admin commands: \n !help \n !get_user \n !ban \n !unban \n !users")
            if entry[0] == "!get_user" and len(entry) > 1:
                buf = self.db_operations(5, entry[1])
                if buf != False:
                    USER.send(f"User info: \n ID: {buf[0][0]} \n Name: {buf[0][1]} \n Rank: {buf[0][3]} \n Status: {buf[0][5]} \n Date of registration: {buf[0][7]} \n [WARN] This is confidential information!")
            if entry[0] == "!ban" and len(entry) >= 4:
                buf = self.db_operations(6, entry[1], entry[2], entry[3])
                if buf:
                    USER.send(f"| USER {entry[1]} was banned for reason: {entry[2]} \n Time: {entry[3]} seconds!")
                    for i in self.users:
                        if i.get_name() == entry[1]:
                            i.get_socket().close()
            if entry[0] == "!unban" and len(entry) > 1:
                buf = self.db_operations(14, entry[1])
                if buf:
                    USER.send(f"| USER {entry[1]} was unbanned!")
            if entry[0] == "!users":
                buf = self.db_operations(15)
                buf1 = "|||||||||||||||||||||||||||| \n LIST: \n"
                counter = 0
                for i in buf:
                    buf1 = buf1 + " " + f"{i[0]}" + f" {i[3]}" + f" {i[5]}" + f" {i[7]} \n"
                    counter += 1
                    if counter == 16:
                        break
                USER.send(f"{buf1}")
        else:
            buf = self.db_operations(13, USER.get_name())
            if buf != False:
                USER.set_rank(buf)               
            else:
                USER.send("| You do not have enough rights for such commands! |")




    def sign(self, user, adr):
        while True:
            try:
                user.send("* Write: login and password or !create login password".encode("utf-8"))
                data = user.recv(2048).decode("utf-8")

                buf0 = "" # Shielding
                for i in data:
                    if i == "'":
                        buf0 = buf0 + "@"
                    else:
                        buf0 = buf0 + i
                data = buf0.split()

                if len(data) > 0:    
                    if data[0] == "!create" and len(data) == 3 and len(data[2]) >= self.userpass_len and len(data[1]) >= self.username_len:  
                        if self.db_operations(3, data[1], data[2]) == True:
                            user.send(f"Login: {data[1]}, created".encode("utf-8"))
                            print (f"[INFO] User connected: {data[1]}")
                            return data[1]
                        else:
                            user.send("* Error! The user already exists!".encode("utf-8"))
                    elif data[0] == "!create" and len(data) == 3 and (len(data[2]) < 6 or len(data[1]) < 4):  
                        user.send("* Error! Name or password is too short!".encode("utf-8"))
                    else:
                        if len(data) == 2:
                            buf = self.db_operations(10, data[0], data[1])
                            if buf == 1:
                                user.send("* Successfully".encode("utf-8"))
                                print (f"[INFO] User connected: {data[0]}")
                                return data[0]
                            elif buf == 0:
                                user.send("Login or password uncorrect.".encode("utf-8"))
                            else:
                                user.send(f"| Your account has been suspended. | \n| Reason: {buf[1]} | \n| Your account will be unblocked: {buf[2]} |".encode("utf-8"))
            except Exception as error:
                print (f"[ERROR] {error}")
                return False

            
    def db_operations(self, *request):
            if len(request) > 0:
                answer = False
                if request[0] == 1:
                    answer = Database.check_init()
                if request[0] == 2:
                    Database.init()
                if request[0] == 3:
                    answer = Database._new_user(request[1], request[2])
                if request[0] == 4:
                    answer = Database._del_user(request[1])
                if request[0] == 5:
                    answer = Database._find_with_name(request[1])
                if request[0] == 6:
                    answer = Database._ban_user(request[1], request[2], request[3])
                if request[0] == 7:
                    answer = Database._set_record(request[1], request[2])
                if request[0] == 8:
                    answer = Database._clear_record(request[1])
                if request[0] == 9:
                    answer = Database._find_with_id(request[1])
                if request[0] == 10:
                    answer = Database._check_name_password(request[1], request[2])
                if request[0] == 11:
                    answer = Database._get_balance(request[1])
                if request[0] == 12:
                    answer = Database._set_balance(request[1], request[2])
                if request[0] == 13:
                    answer = Database._get_rank(request[1])
                if request[0] == 14:
                    answer = Database._unban_user(request[1])
                if request[0] == 15:
                    answer = Database._get_users()
                if request[0] == 16:
                    answer = Database._set_rank(request[1], request[2])
                if request[0] == 17:
                    answer = Database._get_banned_users()
                return answer


    def generate_new_token(self):
        run = True
        while run:
            token = ""
            for i in range(self.token_len):
                token = token + random.choice(self.letters)
            run = False
            for chat in self.chats:
                if chat.get_token() == token:
                    run = True
        return token
