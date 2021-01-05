import json

def encode(data):
    try:
        return json.dumps(data)
    except:
        return data

def decode(data):
    try:
        return json.loads(data)
    except:
        return data
