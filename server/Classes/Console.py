from Classes.Command import Command


class Console:


    @classmethod
    def init(cls, sr):
        print ("* Write !help to get a list of commands")
        while True:
                buf = str(input()).split()
                counter = 0
                for command in sr.commands:
                    if len(buf) > 0 and command["name"] == buf[0]:
                        if len(command["actions"]) > 1:
                            for action in command["actions"]:
                                func = getattr(Command, action["function"])
                                args = action["args"]
                                if len(args) > 0:
                                    for i in range(len(args)):
                                        if args[i] == "#INPUT":
                                            args[i] = input()
                                    func(sr, args)
                                else:
                                    func(sr)
                        elif len(command["actions"]) == 1:
                            func = getattr(Command, command["actions"][0]["function"])
                            args = command["actions"][0]["args"]
                            if len(args) > 0:
                                for i in range(len(args)):
                                        if args[i] == "#INPUT":
                                            args[i] = input()
                                func(sr, args)
                            else:
                                func(sr)
                        else:
                            print ("ACTION NOT FOUND!")
                    else:
                        counter += 1
                if counter == len(sr.commands):
                    print ("Command not found!")


                            #args_list = []
                            #if command["special_flag"]:
                            #    if len(buf[0]) > 1:
                            #        args_list += buf[1:len(buf)]       
                            
