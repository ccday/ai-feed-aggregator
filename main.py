import statistics

import analyzer_gpt
import feed_rss
import sink_stdout
from util import *

feed_registry = {
    'rss': feed_rss.read_feed
}

analyzer_registry = {
    'gpt': analyzer_gpt.analyze
}

sink_registry = {
    'stdout': sink_stdout.write
}


def build_pipeline(config):
    pipeline = {
        'feed_steps': [
            lambda: feed_registry[config['root'][name]['type']](config, name)
            for name in config['feeds']
            if config['root'][name]['enabled'] == 'true'
        ],
        'analyzer_steps': [
            lambda entry: analyzer_registry[config['root'][name]['type']](config, name, entry)
            for name in config['analyzers']
            if config['root'][name]['enabled'] == 'true'
        ],
        'sink_steps': [
            lambda entry: sink_registry[config['root'][name]['type']](config, name, entry)
            for name in config['sinks']
            if config['root'][name]['enabled'] == 'true'
        ]
    }

    debug('pipeline:', pipeline)
    return pipeline


def run_pipeline(config, pipeline):
    max_entries = int(config['root']['global']['max_entries'])
    agg_func = config['root']['global']['relevance_aggregation_function']
    entries = []

    for step in pipeline['feed_steps']:
        entries.extend(step())

    entries = entries[:max_entries]
    debug('entries:', entries)

    for entry in entries:
        relevances = []

        for step in pipeline['analyzer_steps']:
            relevances.append(step(entry))

        if agg_func == 'max': entry['relevance'] = max(relevances)
        if agg_func == 'min': entry['relevance'] = min(relevances)
        if agg_func == 'avg': entry['relevance'] = statistics.mean(relevances)
        if agg_func == 'med': entry['relevance'] = statistics.median(relevances)

        debug('computed relevance:', entry['relevance'], entry)

    for entry in entries:
        for step in pipeline['sink_steps']:
            step(entry)


def main():
    config = load_config()
    pipeline = build_pipeline(config)
    run_pipeline(config, pipeline)


if __name__ == '__main__':
    main()
