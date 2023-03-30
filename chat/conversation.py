from pathlib import Path
from chat.utility import JSON_Manager
import os

class Conversation:
    def __init__(self, uuid, user_name, character_name, inference='default', messages=[]) -> None:
        self.uuid = uuid # Unique User Identifier
        self.messages = messages
        self.inference = inference
        self.user_name = user_name
        self.character_name = character_name

    def clear(self):
        self.messages=[]
        self.baked_snapshot=None

    def save(self, path):
        dir_path = os.path.join(Path(path),f'{self.character_name}')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        JSON_Manager.save_object(self, os.path.join(Path(dir_path),str(self.uuid)))

    def add_message(self, role, text):
        self.messages.append((role, text))

    @staticmethod
    def from_json(path):
        loaded_dict = JSON_Manager.load_object(Path(path))
        return Conversation(**loaded_dict)


# TODO
# Make sure it can save and load
# Create add_message function