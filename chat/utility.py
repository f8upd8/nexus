import json, os
from pathlib import Path

class JSON_Manager:
    @staticmethod
    def save_object(object, path):
        with open(Path(path).with_suffix('.json'), 'wt') as object_json:
            object_json_string = json.dumps(object.__dict__)
            object_json.write(object_json_string)
    @staticmethod
    def load_object(path):
        path = path.with_suffix('.json')
        if not os.path.exists(path):
            return False
        with open(path, 'rt') as object_json_string:
            return json.loads(object_json_string.read())



