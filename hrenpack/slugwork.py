"""
Slug and transliteration utilities.

Provides functions for converting text to slugs (URL-friendly strings)
and transliterating between Cyrillic and Latin alphabets.

Утилиты для создания слаг-строк (дружественных URL) и транслитерации.

Предоставляет функции для преобразования текста в слаг-строки (дружественные URL)
и транслитерации между кириллицей и латиницей.
"""

translit_db = {
    "latin": {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "ye",
        "ё": "yo",
        "ж": "j",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "i",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya"
    },
    "cyrillic": {
        "a": "а",
        "b": "б",
        "c": "ц",
        "d": "д",
        "e": "э",
        "f": "ф",
        "g": "г",
        "h": "х",
        "i": "и",
        "j": "ж",
        "k": "к",
        "l": "л",
        "m": "м",
        "n": "н",
        "o": "о",
        "p": "п",
        "q": "ку",
        "r": "р",
        "s": "с",
        "t": "т",
        "u": "у",
        "v": "в",
        "w": "в",
        "x": "кс",
        "y": "й",
        "z": "з"
    }
}


def translit(data: str, lat_to_cyr: bool = False, translit_no_letters: bool = True) -> str:
    """
    Transliterate between Cyrillic and Latin alphabets.

    Транслитерирует между кириллицей и латиницей.

    Args:
        data (str): Text to transliterate / Текст для транслитерации
        lat_to_cyr (bool): Convert Latin to Cyrillic if True, default False / Преобразовать латиницу в кириллицу
        translit_no_letters (bool): Replace hard/soft signs with hyphens, default True / Заменить твердый/мягкий знаки на дефисы

    Returns:
        str: Transliterated text / Транслитерированный текст
    """
    data = list(data)
    cyrillic = translit_db['cyrillic']
    latin = translit_db['latin']
    if translit_no_letters:
        latin["ъ"] = "-"
        latin["ь"] = "-"
    dictionary = cyrillic if lat_to_cyr else latin
    del cyrillic, latin
    for i in range(len(data)):
        letter = data[i]
        for key in dictionary:
            if letter == key:
                data[i] = dictionary[key]
            if not lat_to_cyr:
                if letter == "Х":
                    data[i] = 'H'
                elif letter == "х":
                    data[i] = 'h'
    return ''.join(data)


def slugify(data: str, translit_no_letters: bool = False) -> str:
    """
    Convert text to URL-friendly slug.

    Преобразует текст в дружественный URL слаг.

    Args:
        data (str): Text to convert / Текст для преобразования
        translit_no_letters (bool): Replace hard/soft signs with hyphens, default False / Заменить твердый/мягкий знаки на дефисы

    Returns:
        str: URL-friendly slug / Дружественный URL слаг
    """
    data = data.lower()
    data = translit(data, translit_no_letters=translit_no_letters)
    ups = list('!@#$%^&*()+=/\\+`~"?{}[] ')
    ups.append('"')
    downs = list('.,<>\n\t\r')
    for i in ups:
        data = data.replace(i, '-')
    for i in downs:
        data = data.replace(i, '_')
    while data[-1] in ('-', '_'):
        data = data[:-1]
    return data
