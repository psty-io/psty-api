import json

def generateOptions(lang_list):
    template = ""
    for i in range(len(lang_list)):
        key = lang_list[i]
        template += '<option value="{}" name="lang">{}</option>'.format(key, key.capitalize())
        template += '\n'
    return template

def createPrivate(filename, password):
    with open('app/private_files.json', 'r+') as json_file:
        data = json.load(json_file)
        data[filename] = {
            'private': True,
            'password': password
        }
        json_file.seek(0)
        json_file.truncate()
        json.dump(data, json_file, indent=4)
        json_file.close()

def checkPassword(password, filename):
    with open('app/private_files.json', 'r+') as json_file:
        data = json.load(json_file)
        r_password = data[filename]['password']
        json_file.close()
    if password != r_password:
        return False
    else:
        return True

def checkPrivate(filename):
    with open('app/private_files.json', 'r+') as json_file:
        data = json.load(json_file)
        array = data.get(filename)
    if array == None:
        return False
    else:
        return True