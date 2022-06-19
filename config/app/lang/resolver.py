import en
import ko

lang_to_module = {'English': en, 'Korean': ko}


def resolve(lang: str, word: str) -> str:
    if lang_to_module.get(lang):
        return lang_to_module[lang].resolve(word)
    return word
