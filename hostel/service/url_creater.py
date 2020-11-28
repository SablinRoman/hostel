def translit_url(room, name):
    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|iu|ia'.split('|')

    trantab = {k: v for k, v in zip(cyrillic, latin)}
    new_url = str(room) + '-'
    for ch in name:
        if ch == ' ':
            new_url += '-'
        else:
            new_url += trantab.get(ch.lower(), ch)

    return new_url


