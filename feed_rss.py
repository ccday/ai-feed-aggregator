from pprint import pprint

import feedparser
import jq

from util import *


def read_feed(config, name):
    feed_config = config['root'][name]
    feed = feedparser.parse(feed_config['url'])

    debug('raw feed:', feed)

    jq_content = jq.compile(feed_config['jq_content'])
    jq_label = jq.compile(feed_config['jq_label'])
    jq_link = jq.compile(feed_config['jq_link'])

    entries = []

    for entry in feed['entries']:
        content = jq_content.input(entry).first()
        label = jq_label.input(entry).first()
        link = jq_link.input(entry).first()

        entries.append({'content': content, 'link': link, 'label': label})

    return entries


def main():
    config = load_config()
    entries = read_feed(config, sys.argv[1])
    pprint(entries)


if __name__ == '__main__':
    main()
