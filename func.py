from translate import Translator

yt = input('Напиши що перекласти:')

translator= Translator(to_lang="uk")
translation = translator.translate(yt)
print(translation)