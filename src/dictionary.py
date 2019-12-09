from PyDictionary import PyDictionary

dictionary = PyDictionary()

def getDefinition(word):
    definition = dictionary.meaning(word)
    result = ""
    for key in definition:
        for meaning in definition[key]:
            result += f'{key} - {meaning}\n'

    return result