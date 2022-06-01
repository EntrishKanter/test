import json



API_TOKEN = '5477259754:AAGppjT48VN5jjytZcLoeqsutZ43vxAxaF8'

NAME_DATA_FILE = 'data'

def GETDATA(NAME_DATA_FILE):
    with open(f'{NAME_DATA_FILE}.txt') as json_file:
        data = json.load(json_file)
        return data

def IS_VALID(NAME_DATA_FILE, name):
    DATA = GETDATA(NAME_DATA_FILE)
    try:
        DATA[str(name)]
        return True
    except:
        return False

def SETDATA(NAME_DATA_FILE, name, data):
    try:
        DATA = GETDATA(NAME_DATA_FILE)
        DATA[str(name)] = str(data)
        with open(f'{NAME_DATA_FILE}.txt', 'w') as outfile:
            json.dump(DATA, outfile)
    except:
        with open(f'{NAME_DATA_FILE}.txt', 'w') as outfile:
            json.dump({str(name) : str(data)}, outfile)








