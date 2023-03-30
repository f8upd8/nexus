from multiprocessing import Process
import glob
import bot_instance
from config.paths import DEFAULT_PATHS
import os
from pathlib import Path


def worker(persona_name):
    bot_instance.run(persona_name)

def load_bots():
    bot_processes = []
    for bot_json in glob.glob(os.path.join(Path(DEFAULT_PATHS.CHARACTERS), '*.json')):
        bot_name = bot_json.split('/')[-1].split('.')[0]  
        print(bot_name)
        bp = Process(target=worker, args=(bot_name,))
        bp.start()
        bot_processes.append(bp)
    for bot_process in bot_processes:
        bot_process.join() # I have no idea what it does with all my honesty


load_bots()