import os
import json


def read_file(filename):
    path = ""
    filepath = os.path.join(path, filename)
    with open(filepath, 'r') as f:
        if filename.endswith(".json"):
            return json.load(f)
        else:
            if 'hand' in filename or 'cartes' in filename:
                return [int(c) for c in f.read().split("\n")[:-1]]
            elif 'historic' in filename:
                return int(f.read().split('\n')[-1])
            else:
                return f.read()


def write_file(filename, content):
    path = ""
    filepath = os.path.join(path, filename)
    if 'historic' in filename:
        with open(filepath, 'a') as f:
            f.write("\n{}".format(content))
    else:
        with open(filepath, 'w') as f:
            if isinstance(content, list):
                for i in content:
                    f.write('{}\n'.format(i))

            elif 'state' in filename or 'player' in filename:
                f.write(str(content))

            elif filename.endswith('.json'):
                json.dump(content, f)
