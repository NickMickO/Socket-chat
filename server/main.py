import json
import sys



import Logger
from Classes.Server import Server




default_command = [
                        {
                            "name":"default",
                            "actions":[{"function":"func", "args":[]}],
                            "special_flag":False
                        }
                ]




def init(*args):
    global default_settings
    settings = default_settings
    
    mainLogger = Logger("mainLogger", True)


    try:
        with open("commands.json", "r") as commands_file:
            commands_list = json.load(commands_file)
    except FileNotFoundError:
        with open("commands.json", "w") as commands_file:
            commands_list = [{"name":"ping", "actions":[{"function":"ping", "args":[]}] ,"rights":2, "special_flag":False}]
            json.dump(commands_list, commands_file)
    try:
        with open("admin_ranks.json", "r") as ranks_file:
            ranks_list = json.load(ranks_file)
    except FileNotFoundError:
        with open("admin_ranks.json", "w") as ranks_file:
            ranks_list = [{
                    "name":"HOST",
                    "rank":8,
                    "permissions":["stats", "stop"]
                },
                {
                    "name":"ADMIN",
                    "rank":6,
                    "permissions":["ban", "unban", "get_bans"]
                },
                {
                    "name":"TEST",
                    "rank":2,
                    "permissions":["help"]
                }
            ]
            json.dump(ranks_list, ranks_file)
    sr = Server(settings, default_settings["version"], commands_list, ranks_list)
    input()


if __name__ == "__main__":
    init(sys.argv)