def generateOptions(dictionary):
    template = ""
    for key, value in sorted(dictionary.items()):
        template += '<option value="{}" name="lang">{}</option>'.format(key, key)
        template += '\n'
    return template
