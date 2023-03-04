# AI Feed Aggregator

1. Pull data from a feed.
2. Analyze it, optionally with AI.
3. Send it somewhere.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

All configuration is in config.ini. You should only need to change a few values to get started:

1. Set `interest.natural_language` to a natural language description of the content you are interested in seeing, for
   example: "I am interested the war in Ukraine, particularly in its humanitarian impact."
2. Set `analyzer.gpt.api_key` to your OpenAI API key [located here](https://platform.openai.com/account/api-keys).
   You can [register for an account with free credit](https://platform.openai.com/signup). 

## Running

```bash
python main.py
```

## Feeds

The only currently supported feed type is RSS. For example, to add a feed for world news from The Guardian:

```
[feed.guardian_world]
type = rss
enabled = true

url = https://www.theguardian.com/world/rss
jq_content = .summary
jq_label = .title
jq_link = .link
```

The `jq` options should be a [jq query](https://stedolan.github.io/jq/manual/) that resolves to the content,
label/title, and link of the RSS entry.

You can run `python feed_rss.py feed.guardian_world` to see the structure of the entries.

## Analyzers

Analyzers decide whether some content is relevant to you. The only current analyzer is `analyzer.gpt` which uses
OpenAI's `gpt-3.5-turbo` model to score the content between 0 and 1 according to your interests. This is the same
model that underlies ChatGPT. You can configure the prompt and inference parameters in config.ini.

## Sinks

Sinks output the entries along with their relevance. The only current sink is stdout which will print entries, their
relevance, and their link to stdout. You can set a relevance threshold to filter the output by in config.ini.
