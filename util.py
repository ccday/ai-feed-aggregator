import configparser
import sys

DEBUG_ENABLED = False


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    set_debug(config.get('global', 'debug_enabled').lower() == 'true')
    debug({section: dict(config[section]) for section in config.sections()})

    def get_sections_by_pfx(pfx):
        return [section for section in config.sections() if section.startswith(pfx)]

    parsed = {
        'root': config,
        'feeds': get_sections_by_pfx('feed.'),
        'analyzers': get_sections_by_pfx('analyzer.'),
        'sinks': get_sections_by_pfx('sink.')
    }

    debug(parsed)

    def print_section(section):
        info(f'Found {section}:', ', '.join(parsed[section]).split('.')[1])

    print_section('feeds')
    print_section('analyzers')
    print_section('sinks')

    return parsed


def set_debug(enabled):
    global DEBUG_ENABLED
    DEBUG_ENABLED = enabled


def debug(*args):
    if DEBUG_ENABLED: print('debug:', *args, file=sys.stderr)


def info(*args):
    print(*args, file=sys.stderr)


def error(*args, should_exit=False):
    print('error:', *args, file=sys.stderr)
    if should_exit: exit(1)


def template(tpl: str, config, entry):
    templated = tpl.replace('{interest.natural_language}', config['root']['interest']['natural_language'])
    templated = templated.replace('{entry.label}', entry['label'])
    templated = templated.replace('{entry.content}', entry['content'])
    return templated
