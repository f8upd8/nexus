import discord
from config.bot_tokens import BOT_TOKENS
from chat import Persona, Conversation
from config.paths import DEFAULT_PATHS
from pathlib import Path
from chat.composer import Composer
from config.openai_config import DEFAULT_SYSPROMPT
from inference.openai_api_inference import oai_completion_inference
import re

PERSONA = None
CONVERSATIONS = []

def fix_mentions(message):
    for mention in re.finditer(r'<@!?(\d+)>', message.content):
        user_id = int(mention.group(1))
        print(user_id)
        member = discord.utils.get(message.guild.members, id=user_id)
        if member:
            return message.content.replace(mention.group(0), f"@{member.name}")
        return message.content
    return message.content

class CharBot(discord.Client):
    async def on_ready(self):
        global CONVERSATIONS
        print(f'[{PERSONA.name}]: Logged on as {self.user}!')
        CONVERSATIONS = PERSONA.load_conversations()
        print(f'[{PERSONA.name}]: Loaded {len(CONVERSATIONS)} conversations.')

    async def on_message(self, message):
        global PERSONA
        if message.author == self.user:
            return
        if (self.user in message.mentions) or not message.guild:
            if CONVERSATIONS.get(message.author.id):
                CONVERSATIONS[message.author.id].add_message('user', fix_mentions(message))
            else:
                CONVERSATIONS[message.author.id] = Conversation(message.author.id, message.author.name, PERSONA.name)
                CONVERSATIONS[message.author.id].add_message('user', message.content)
            completion = self.reply(CONVERSATIONS[message.author.id],message.author.name)
            CONVERSATIONS[message.author.id].add_message('char', completion)
            CONVERSATIONS[message.author.id].save(Path(DEFAULT_PATHS.CHATS))
            await message.channel.send(completion, reference=message)

    def reply(self, conversation, username):
        global PERSONA
        prompt = Composer.davinci_completion(PERSONA,conversation,DEFAULT_SYSPROMPT)
        completion = oai_completion_inference(prompt, username)
        return completion

def run(persona_name):
    global PERSONA
    intents = discord.Intents.default()
    intents.message_content = True
    PERSONA = Persona.from_json(Path(DEFAULT_PATHS.CHARACTERS), persona_name)
    client = CharBot(intents=intents)
    client.run(BOT_TOKENS.get(PERSONA.name.lower().replace(' ','_'))) # TODO Make a more mindful filenaming