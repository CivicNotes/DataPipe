import argparse
from glob import glob
from os.path import join
import re
import json

STASH_PATH = join('stash', 'fetched')


def check_file_for_match(filename, pattern):
    with open(filename, 'r') as f:
        for i, txt in enumerate(f):
            mtch = re.search(pattern, txt)
            if mtch:
                return {'text': txt, 'filename': filename, 'line_number': i + 1}
    return False

def get_filenames():
    return glob(join(STASH_PATH, '*.txt'))


def search_all_files_for_pattern(pattern):
    matches = []
    for tname in get_filenames():
        matchobj = check_file_for_match(tname, pattern)
        if matchobj:
           matches.append(matchobj)
    return matches



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="pattern to search for")
    args = parser.parse_args()
    pattern = args.pattern
    print("Searching for", pattern, '...')

    matches = search_all_files_for_pattern(pattern)
    print("Found", len(matches))
    print(json.dumps(matches, indent=2))
