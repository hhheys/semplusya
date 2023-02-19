import json


def add_user(tg_id,group):
    if not user_exists(tg_id):
        json_data = {
            "tg_id": tg_id,
            "group": group,
        }
        data = json.load(open("data.json"))
        data['users'].append(json_data)
        with open("data.json", "w", encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

def get_user_class(tg_id):
    data = json.load(open("data.json", encoding='utf-8'))
    for i in data['users']:
        if i['tg_id'] == tg_id:
            return i['group']

def get_users():
    data = json.load(open("data.json", encoding='utf-8'))
    users = []
    for i in data['users']:
        users.append(i)
    return users

def user_exists(tg_id):
    data = json.load(open("data.json", encoding='utf-8'))
    exist = False
    for i in data['users']:
        if i['tg_id'] == tg_id:
            exist = True
    return exist

def admin_exists(tg_id):
    data = json.load(open("data.json", encoding='utf-8'))
    exist = False
    for i in data['admins']:
        if i['tg_id'] == tg_id:
            exist = True
    return exist