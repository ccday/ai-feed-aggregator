import json

import openai

from util import *


def analyze(config, name, entry):
    analyzer_config = config['root'][name]
    openai.api_key = analyzer_config['api_key']
    strategy = analyzer_config['strategy']

    if strategy == 'natural_language_oneshot':
        return _natural_language_oneshot(config, name, entry)
    else:
        error('unknown GPT strategy:', strategy)
        return 0


def _natural_language_oneshot(config, name, entry):
    analyzer_config = config['root'][name]

    def tpl(val):
        return template(val, config, entry)

    messages = [
        {'role': 'system', 'content': tpl(analyzer_config['prompt_system'])},
        {'role': 'user', 'content': tpl(analyzer_config['prompt_interests'])},
        {'role': 'user', 'content': tpl(analyzer_config['prompt_content'])},
        {'role': 'user', 'content': tpl(analyzer_config['prompt_query'])}
    ]

    debug('GPT prompt:', messages)

    response = openai.ChatCompletion.create(
        model=analyzer_config['model'],
        messages=messages,
        temperature=float(analyzer_config['temperature']),
        max_tokens=int(analyzer_config['max_tokens'])
    )

    message: str = response['choices'][0]['message']['content']
    debug('GPT response:', message)

    try:
        return float(message)
    except ValueError:
        error('no number found in GPT response, check prompt')
        return float(0)


def main(name, entry):
    config = load_config()
    relevance = analyze(config, name, entry)
    print(relevance)


if __name__ == '__main__':
    main(sys.argv[1], json.loads(sys.argv[2]))
