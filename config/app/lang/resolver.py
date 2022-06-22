from config.app.appconfig import AppConfiguration
from config.app.lang import en
from config.app.lang import ko

config = AppConfiguration()
lang_to_module = {'English': en, 'Korean': ko}


def resolve(word: str, lang: str = None) -> str:
    if not lang:
        lang = config.get('system', 'language')
    if lang_to_module.get(lang):
        return lang_to_module[lang].resolve(word)
    return word
