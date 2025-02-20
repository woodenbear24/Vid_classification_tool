import json

def tag_load():
    try:
        with open("tags.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        with open("tags.json", 'w', encoding='utf-8')as f:
            data = {"author":[], "tag":[]}
            json.dump(data, f, indent=2, ensure_ascii=False)
    return data

def tag_save(data):
    try:
        with open("tags.json", 'w', encoding='utf-8')as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        print(f"err saving tags:{Exception}")
    return
