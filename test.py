from translate import Translator
from dictionary import *
# Створюємо екземпляр перекладача для перекладу з української на англійську
translator = Translator(from_lang='uk', to_lang='en')
res = ''
# Зчитуємо речення з input
sentence = input("Введіть речення: ")

# Розбиваємо речення на слова і переносимо їх у список
words = sentence.split()
             
for word in words:
    tr = word
    if tr in vocabulary.keys():
        tr = vocabulary[word]
    else:
        tr = translator.translate(word)
    res += tr + ' '
    
# Виводимо перекладені слова
print("Перекладені слова:", res)
