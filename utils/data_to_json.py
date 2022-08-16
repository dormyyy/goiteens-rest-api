import json


def to_json(data):
    f = open('data.json', 'r+', encoding='utf-8')
    json_file = json.load(f)
    json_file.append(data)
    json_data = json.dumps(json_file, indent=4, ensure_ascii=False)
    f = open('data.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()
