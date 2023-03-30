class Composer:
    @staticmethod
    def davinci_completion(persona, conversation, sysprompt):
        character_prompt = persona.character_prompt
        sysprompt = sysprompt.replace('{{char}}', persona.name)
        message_history = list(map(lambda x: f'{conversation.user_name}: {x[1]}' if x[0]=='user' else f'{persona.name}: {x[1]}', conversation.messages))
        message_history.append(f'{persona.name}:')
        message_history = '\n'.join(message_history)
        message_history = '<START OF ROLEPLAY CHAT>\n' + message_history
        return '\n'.join([f'[{sysprompt}]',character_prompt,message_history])
    @staticmethod
    def turbo3_chat_completion(persona, conversation, sysprompts, inference):
        pass
    @staticmethod
    def llama_completion(persona, conversation, sysprompts, inference):
        pass

# TODO
# Test what composed general_completion looks like