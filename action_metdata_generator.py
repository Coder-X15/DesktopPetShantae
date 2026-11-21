import json
import os
import sys

def crawl(path : str) -> dict[str, list]:
    ''' crawls through your sprite directory, compiles its actions and generates a metadata file (JSON)'''
    action_dict = dict()
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if action_dict.get(dir) is None:
                action_dict[dir] = []

        try:
            emote = root.split('/')
            for file in files:
                action_dict[emote[2]].append(os.path.join(root, file))
            action_dict[emote[2]] = sorted(action_dict[emote[2]])
        except Exception:
            pass

    return action_dict

if __name__ == "__main__":
    res = crawl(sys.argv[1])
    filename = sys.argv[2] + '.json'
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(res, file, indent=1)
    