import json



def GETDATA(NAME_DATA_FILE):
    with open(f'{NAME_DATA_FILE}.txt', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def IS_VALID(NAME_DATA_FILE, name):
    try:
        DATA = GETDATA(NAME_DATA_FILE)
        DATA[str(name)]
        return True
    except:
        return False

def SETDATA(NAME_DATA_FILE, name, data):
    try:
        DATA = GETDATA(NAME_DATA_FILE)
        DATA[str(name)] = str(data)
        with open(f'{NAME_DATA_FILE}.txt', 'w', encoding='utf-8') as outfile:
            json.dump(DATA, outfile)
    except:
        with open(f'{NAME_DATA_FILE}.txt', 'w', encoding='utf-8') as outfile:
            json.dump({str(name) : str(data)}, outfile)


