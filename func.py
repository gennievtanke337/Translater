from translate import Translator

yt = input('Напиши що перекласти:')
lang = input() #combo box 
translator= Translator(from_lang='uk',to_lang=lang)
translation = translator.translate(yt)
print(translation)