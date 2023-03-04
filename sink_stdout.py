def write(config, name, entry):
    threshold = float(config['root'][name]['relevance_threshold'])

    if entry['relevance'] >= threshold:
        print(f'{entry["label"]} ({entry["relevance"]}):', entry['link'])
