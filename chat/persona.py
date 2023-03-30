from pathlib import Path
from chat import Conversation
from chat.utility import JSON_Manager
from config.paths import DEFAULT_PATHS
import glob, os

class Persona:
    def __init__(self, name, character_prompt, sysprompts_override=None) -> None:
        self.sysprompts_override = sysprompts_override
        self.character_prompt = character_prompt
        self.name = name

    def save(self, path):
        JSON_Manager.save_object(self, Path(path).joinpath(self.name.lower().replace(' ','_')))

    def load_conversations(self):
        conversations = {}
        dir_path = os.path.join(DEFAULT_PATHS.CHATS, f'{self.name}')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            return conversations
        for conversation_json_file in glob.glob(os.path.join(dir_path, '*.json')):
            conversation = Conversation.from_json(conversation_json_file)
            conversations[conversation.uuid] = conversation
        return conversations

    @staticmethod
    def from_json(path, name):
        loaded_dict = JSON_Manager.load_object(Path(path).joinpath(name.lower().replace(' ','_')))
        return Persona(**loaded_dict)