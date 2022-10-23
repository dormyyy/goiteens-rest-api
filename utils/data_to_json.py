import json
import datetime

def to_json(data):
    f = open('data.json', 'r+', encoding='utf-8')
    json_file = json.load(f)
    json_file.append(data)
    json_data = json.dumps(json_file, indent=4, ensure_ascii=False)
    f = open('data.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()

def to_json_test(data):
    f = open('data_test.json', 'r+', encoding='utf-8')
    json_file = json.load(f)
    json_file.append(data)
    json_data = json.dumps(json_file, indent=4, ensure_ascii=False)
    f = open('data_test.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()
    return json_data

def data_slot_update(manager_id_out=0,manager_id_in=0,slot_id_out=0,slot_id_in=0):
    f = open('data_slot_update.json', 'r+', encoding='utf-8')
    json_file = json.load(f)
    ln = len(json_file)
    now = datetime.datetime.now()
    dt = {
            "id": ln,
            "manager_id_out": manager_id_out,
            "manager_id_in": manager_id_in,
            "slot_id_out":slot_id_out,
            "slot_id_in":slot_id_in,
            "date-time": str(now)
        }
    json_file.append(dt)
    json_data = json.dumps(json_file, indent=4, ensure_ascii=False)
    f = open('data_slot_update.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()
    print(json_data)
    return json_data