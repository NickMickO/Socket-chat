import json
import logging
import logging.config
import os

class Logger:
    
    def __init__(self, name="root", debbag=False, filename="main.log"):
        self.name = name
        self.filename = filename
        self.logger_object = logging.getLogger(name)
        if debbag:
            self.logger_object.setLevel(logging.INFO)
        else:
            self.logger_object.setLevel(logging.WARNING)
        self.handler = logging.FileHandler(f"{name}.log", mode='w')
        self.formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger_object.addHandler(self.handler)
        self.logger.info(f"Testing the custom logger for module {name}...")

    @staticmethod
    def CreateLogFolder(self, folder="logs"):
        if not os.path.exists(folder):
            os.mkdir(folder)

