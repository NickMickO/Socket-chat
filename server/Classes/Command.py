class Command:

    @staticmethod
    def ping(sr):
        print ("pong")

    @staticmethod
    def get_users(sr):
            print ("USERS LIST: \n")
            for i in sr.users:
                print (i.get_pid())
                print (i.get_uid())
                print (i.get_name())
                print (i.get_rank())

    @staticmethod
    def help(sr):
        print ("* Control console ** help \n List with commands: \n !help \n !stop \n !users \n !stats \n !close \n !chats \n !ban \n !unban \n !get_user \n !gvadmin \n !deadmin \n !bans \n []")

    @staticmethod
    def stop(sr):
        print ("[WARN] Stopping SERVER!")
        print ("[INFO] SERVER stopped")
        sr.active = False
        sr.server.close()

    @staticmethod
    def get_bans(sr):
        print ("BANS LIST: \n")
        for i in sr.db_operations(17):
            print (i[0])
            print (i[1])
            print (i[2])

    @staticmethod
    def setrank(sr, args):
        buf1 = sr.db_operations(5, args[0])
        if len(buf1) == 2:
            sr.db_operations(16, args[0], 2)
            print ("[LOG] Administrator rights granted!")
        elif len(buf1) == 3:
            sr.db_operations(16, args[0], args[1])
            print (f"[LOG] Set new rank for user: {args[1]}!")
        else:
            print ("[ERROR] User is not found!")

    @staticmethod
    def deadmin(sr, args):
        buf1 = sr.db_operations(5, args[0])
        if len(buf1) >= 1:
            sr.db_operations(16, args[0], 0)
            print ("[LOG] Administrator rights removed!")
        else:
            print ("[ERROR] User is not found!")

    @staticmethod
    def get_chats(sr):
        print ("CHATS INFO:")
        print ("Count: ", len(sr.chats))
        print ("List:\n")
        for i in sr.chats:
            print (f"Chat: {i.get_name()}")
            print (f"Owner: {i.get_owner()}")
            print (f"Token: {i.get_token()}")
            print (f"Count of members: {len(i.get_members())}")
            print ("|||||||||||||||||||||||")

    @staticmethod
    def get_stats(sr):
        print (f"SERVER version {sr.version}")
        print (f"ADDRESS: {sr.ip}, PORT: {sr.port}")

    @staticmethod
    def get_user(sr, args):
        buf1 = sr.db_operations(5, args[0])[0]
        print (f"User info: \n ID: {buf1[0]} \n Name: {buf1[1]} \n Rank: {buf1[3]} \n Balance: {buf1[4]} \n Status: {buf1[5]} \n Date of registration: {buf1[7]}")

    @staticmethod
    def ban(sr, args):
        buf1 = sr.db_operations(6, args[0], args[1], args[2])
        if buf1:
            print (f"| USER {args[0]} was banned for reason: {args[1]} \n Time: {args[2]} seconds!")
            for i in sr.users:
                if i.get_name() == args[0]:
                    i.get_socket().close()
                else:
                    print ("[ERROR] Unable to perform operation!")

    @staticmethod
    def unban(sr, args):
        buf1 = sr.db_operations(14, args[0])
        if buf1:
            print (f"| USER {args[0]} was unbanned!")
        else:
            print ("[ERROR] Unable to perform operation!")
