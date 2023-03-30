import openai

from config import api_keys, openai_config


def oai_completion_inference(prompt,
                                   user_name,
                                   parameters=openai_config.DEFAULT_PARAMETERS,
                                   api_key=api_keys.OPENAI_KEY,
                                   model='gpt-3.5-turbo'):
    openai.api_key = api_key
    print(prompt)
    completion = openai.Completion.create(prompt=prompt,
                                              stop=f'\n{user_name}',
                                              **parameters)
    return completion.choices[0].text

# TODO
# Test if it works at all for any completion