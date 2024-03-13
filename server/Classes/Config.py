import json



"""

This class creates the configuration if it does not exist. 
Loads data from the config, processes input from the console, 
and also passes the received settings from the config to the Server class to start working.

"""


class Config:

    # Default
    VERSION = "0.6.0"
    DEFAULT_MAX_USERS = 99
    DEFAULT_IP = '127.0.0.1'
    DEFAULT_PORT = 8001
    DEFAULT_TOKEN_LEN = 12 # Chat token
    DEFAULT_MAX_CHATS = 99
    DEFAULT_GLOBAL_CHAT = True
    DEFAULT_USERNAME_LEN = 4
    DEFAULT_USERPASS_LEN = 6
    DEFAULT_MINADMIN_RANK = 2
    DEFAULT_MAXADMIN_RANK = 8
    DEFAULT_DEBBAG = False
    DEFAULT_GUESTS = False

    default_settings = {
        "version":VERSION, 
        "ip":DEFAULT_IP, 
        "port":DEFAULT_PORT, 
        "max_users":DEFAULT_MAX_USERS,
        "max_chats":DEFAULT_MAX_CHATS,
        "token_len":DEFAULT_TOKEN_LEN,
        "global_chat":DEFAULT_GLOBAL_CHAT,
        "username_len":DEFAULT_USERNAME_LEN,
        "userpass_len":DEFAULT_USERPASS_LEN,
        "minadmin_rank":DEFAULT_MINADMIN_RANK,
        "maxadmin_rank":DEFAULT_MAXADMIN_RANK,
        "debbag":DEFAULT_DEBBAG,
        "guests":DEFAULT_GUESTS
    }


    @classmethod
    def CreateSettingsObject(cls):
        settings = cls.default_settings
        return settings

    @classmethod
    def HandleConsoleInput(cls, args):
        settings = cls.CreateSettingsObject()
        if len(args)>=3:
            try:
                settings["ip"] = int([1])
                settings["port"] = int([2])
                settings["debbag"] = bool([3])
                console_args = True
            except Exception as err:
                print (err)
                input()
        else:
            console_args = False
        return console_args, settings


    @classmethod
    def PrepareSettings(cls, settings):

            try:
                print ("[LOG] Open config")
                with open("server_config.json", "r") as config:
                    settings = json.load(config)
            except Exception as error:
                print ("[ERROR] Config not found!")
                with open("server_config.json", "w") as config:
                    json.dump(default_settings, config) 


