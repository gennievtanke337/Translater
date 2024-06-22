from PyQt5 import QtWidgets, QtCore, QtGui
from translate import Translator

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Налаштування')
        self.resize(400, 300)

        self.layout = QtWidgets.QVBoxLayout()

        self.lang_label = QtWidgets.QLabel('Оберіть мову інтерфейсу:')
        self.lang_combobox = QtWidgets.QComboBox()
        self.lang_combobox.addItems(['Українська', 'English'])
        self.layout.addWidget(self.lang_label)
        self.layout.addWidget(self.lang_combobox)

        self.color_label = QtWidgets.QLabel('Оберіть кольорову схему:')
        self.color_combobox = QtWidgets.QComboBox()
        self.color_combobox.addItems(['Світла', 'Темна', 'Користувацька'])
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_combobox)

        self.custom_color_button = QtWidgets.QPushButton('Оберіть колір...')
        self.custom_color_button.clicked.connect(self.choose_color)
        self.custom_color_button.setEnabled(False)
        self.layout.addWidget(self.custom_color_button)

        self.color_combobox.currentTextChanged.connect(self.toggle_custom_color)

        self.ok_button = QtWidgets.QPushButton('OK')
        self.ok_button.clicked.connect(self.apply_settings)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

        self.custom_color = None

    def toggle_custom_color(self, text):
        self.custom_color_button.setEnabled(text == 'Користувацька')

    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.custom_color = color

    def apply_settings(self):
        language = self.lang_combobox.currentText()
        color_scheme = self.color_combobox.currentText()

        settings = {
            'language': language,
            'color_scheme': color_scheme,
            'custom_color': self.custom_color
        }
        self.parent.apply_settings(settings)
        self.accept()

class TranslatorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.setModal(True)

        self.settings = {
            'language': 'English',  # Дефолтна мова програми
            'color_scheme': 'Світла',
            'custom_color': None
        }
        self.load_settings()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Перекладач')
        self.resize(800, 600)

        self.layout = QtWidgets.QVBoxLayout()

        self.src_lang_label = QtWidgets.QLabel('Мова оригіналу:')
        self.src_lang_combobox = QtWidgets.QComboBox()
        self.src_lang_combobox.addItem('Англійська', 'en')
        self.src_lang_combobox.addItem('Українська', 'uk')
        self.src_lang_combobox.addItem('Російська', 'ru')
        self.src_lang_combobox.addItem('Французька', 'fr')
        self.src_lang_combobox.addItem('Німецька', 'de')
        self.src_lang_combobox.addItem('Іспанська', 'es')
        self.src_lang_combobox.addItem('Італійська', 'it')
        self.src_lang_combobox.addItem('Польська', 'pl')
        self.src_lang_combobox.addItem('Японська', 'ja')
        self.src_lang_combobox.addItem('Китайська', 'zh')
        self.src_lang_combobox.addItem('Корейська', 'ko')
        self.layout.addWidget(self.src_lang_label)
        self.layout.addWidget(self.src_lang_combobox)

        self.dest_lang_label = QtWidgets.QLabel('Мова перекладу:')
        self.dest_lang_combobox = QtWidgets.QComboBox()
        self.dest_lang_combobox.addItem('Англійська', 'en')
        self.dest_lang_combobox.addItem('Українська', 'uk')
        self.dest_lang_combobox.addItem('Російська', 'ru')
        self.dest_lang_combobox.addItem('Французька', 'fr')
        self.dest_lang_combobox.addItem('Німецька', 'de')
        self.dest_lang_combobox.addItem('Іспанська', 'es')
        self.dest_lang_combobox.addItem('Італійська', 'it')
        self.dest_lang_combobox.addItem('Польська', 'pl')
        self.dest_lang_combobox.addItem('Японська', 'ja')
        self.dest_lang_combobox.addItem('Китайська', 'zh')
        self.dest_lang_combobox.addItem('Корейська', 'ko')
        self.layout.addWidget(self.dest_lang_label)
        self.layout.addWidget(self.dest_lang_combobox)

        self.src_text_label = QtWidgets.QLabel('Введіть текст:')
        self.src_text_box = QtWidgets.QTextEdit()
        self.src_text_box.setMinimumHeight(200)
        self.layout.addWidget(self.src_text_label)
        self.layout.addWidget(self.src_text_box)

        self.translate_button = QtWidgets.QPushButton('Перекласти')
        self.translate_button.setMinimumHeight(50)
        self.translate_button.setStyleSheet("font-size: 18px;")
        self.translate_button.clicked.connect(self.translate_text)
        self.layout.addWidget(self.translate_button)

        self.dest_text_label = QtWidgets.QLabel('Переклад:')
        self.dest_text_box = QtWidgets.QTextEdit()
        self.dest_text_box.setMinimumHeight(200)
        self.dest_text_box.setReadOnly(True)
        self.layout.addWidget(self.dest_text_label)
        self.layout.addWidget(self.dest_text_box)

        self.apply_settings()

        self.settings_button = QtWidgets.QPushButton('Налаштування')
        self.settings_button.clicked.connect(self.show_settings_dialog)
        self.layout.addWidget(self.settings_button)

        self.setLayout(self.layout)

    def load_settings(self):
        pass

    def apply_settings(self, settings=None):
        if settings:
            self.settings = settings

        lang_index = self.src_lang_combobox.findData(self.settings['language'])
        if lang_index != -1:
            self.src_lang_combobox.setCurrentIndex(lang_index)
        lang_index = self.dest_lang_combobox.findData(self.settings['language'])
        if lang_index != -1:
            self.dest_lang_combobox.setCurrentIndex(lang_index)

        color_scheme = self.settings['color_scheme']
        if color_scheme == 'Темна':
            self.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        elif color_scheme == 'Користувацька' and self.settings['custom_color']:
            custom_color = self.settings['custom_color']
            self.setStyleSheet(f"background-color: {custom_color.name()}; color: #FFFFFF;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: #000000;")

    def show_settings_dialog(self):
        self.settings_dialog.exec_()

    def translate_text(self):
        src_text = self.src_text_box.toPlainText().strip()
        src_lang = self.src_lang_combobox.currentData()
        dest_lang = self.dest_lang_combobox.currentData()

        if src_text:
            exceptions = {
                'en': {
                    'everyone': 'всім',
                    'relax': 'чіл',
                    'potato': 'бульба',
                    'potatoes': 'бульби',
                    'movie': 'фільм',
                    'funny': 'смішно',
                    'a lot': 'багато',
                    'my friend': 'мій друже',
                    'good afternoon': 'добрий день',
                    'house': 'будинок',
                    'school': 'школа',
                    'child': 'дитина',
                    'man': 'чоловік',
                    'woman': 'жінка',
                    'work': 'робота',
                    'car': 'машина',
                    'I am': 'я',
                    'you are': 'ти',
                    'he is': 'він',
                    'she is': 'вона',
                    'they are': 'вони'
                },
                'uk': {
                    'всім': 'everyone',
                    'чіл': 'relax',
                    'бульба': 'potato',
                    'бульби': 'potatoes',
                    'бульбу': 'potato',
                    'фільм': 'movie',
                    'смішно': 'funny',
                    'багато': 'a lot',
                    'мій друже': 'my friend',
                    'добрий день': 'good afternoon',
                    'будинок': 'house',
                    'школа': 'school',
                    'дитина': 'child',
                    'чоловік': 'man',
                    'жінка': 'woman',
                    'робота': 'work',
                    'машина': 'car',
                    'я': 'I am',
                    'ти': 'you are',
                    'він': 'he is',
                    'вона': 'she is',
                    'вони': 'they are'
                },
                'ru': {
                    'всем': 'everyone',
                    'расслабиться': 'relax',
                    'картошка': 'potato',
                    'картошки': 'potatoes',
                    'фильм': 'movie',
                    'смешно': 'funny',
                    'много': 'a lot',
                    'мой друг': 'my friend',
                    'добрый день': 'good afternoon',
                    'дом': 'house',
                    'школа': 'school',
                    'ребенок': 'child',
                    'мужчина': 'man',
                    'женщина': 'woman',
                    'работа': 'work',
                    'машина': 'car',
                    'я': 'I am',
                    'ты': 'you are',
                    'он': 'he is',
                    'она': 'she is',
                    'они': 'they are'
                },
                'fr': {
                    'tout le monde': 'everyone',
                    'se détendre': 'relax',
                    'pomme de terre': 'potato',
                    'pommes de terre': 'potatoes',
                    'film': 'movie',
                    'drôle': 'funny',
                    'beaucoup': 'a lot',
                    'mon ami': 'my friend',
                    'bon après-midi': 'good afternoon',
                    'maison': 'house',
                    'école': 'school',
                    'enfant': 'child',
                    'homme': 'man',
                    'femme': 'woman',
                    'travail': 'work',
                    'voiture': 'car',
                    'je suis': 'I am',
                    'tu es': 'you are',
                    'il est': 'he is',
                    'elle est': 'she is',
                    'ils sont': 'they are'
                },
                'de': {
                    'jeder': 'everyone',
                    'entspannen': 'relax',
                    'kartoffel': 'potato',
                    'kartoffeln': 'potatoes',
                    'film': 'movie',
                    'lustig': 'funny',
                    'viel': 'a lot',
                    'mein freund': 'my friend',
                    'guten tag': 'good afternoon',
                    'haus': 'house',
                    'schule': 'school',
                    'kind': 'child',
                    'mann': 'man',
                    'frau': 'woman',
                    'arbeit': 'work',
                    'auto': 'car',
                    'ich bin': 'I am',
                    'du bist': 'you are',
                    'er ist': 'he is',
                    'sie ist': 'she is',
                    'sie sind': 'they are'
                },
                'es': {
                    'todos': 'everyone',
                    'relajar': 'relax',
                    'patata': 'potato',
                    'patatas': 'potatoes',
                    'película': 'movie',
                    'divertido': 'funny',
                    'mucho': 'a lot',
                    'mi amigo': 'my friend',
                    'buenas tardes': 'good afternoon',
                    'casa': 'house',
                    'escuela': 'school',
                    'niño': 'child',
                    'hombre': 'man',
                    'mujer': 'woman',
                    'trabajo': 'work',
                    'coche': 'car',
                    'soy': 'I am',
                    'eres': 'you are',
                    'él es': 'he is',
                    'ella es': 'she is',
                    'ellos son': 'they are'
                },
                'it': {
                    'tutti': 'everyone',
                    'rilassati': 'relax',
                    'patata': 'potato',
                    'patate': 'potatoes',
                    'film': 'movie',
                    'divertente': 'funny',
                    'molto': 'a lot',
                    'mio amico': 'my friend',
                    'buon pomeriggio': 'good afternoon',
                    'casa': 'house',
                    'scuola': 'school',
                    'bambino': 'child',
                    'uomo': 'man',
                    'donna': 'woman',
                    'lavoro': 'work',
                    'auto': 'car',
                    'io sono': 'I am',
                    'tu sei': 'you are',
                    'egli è': 'he is',
                    'lei è': 'she is',
                    'loro sono': 'they are'
                },
                'pl': {
                    'wszyscy': 'everyone',
                    'relaks': 'relax',
                    'ziemniak': 'potato',
                    'ziemniaki': 'potatoes',
                    'film': 'movie',
                    'śmieszny': 'funny',
                    'dużo': 'a lot',
                    'mój przyjaciel': 'my friend',
                    'dzień dobry': 'good afternoon',
                    'dom': 'house',
                    'szkoła': 'school',
                    'dziecko': 'child',
                    'mężczyzna': 'man',
                    'kobieta': 'woman',
                    'praca': 'work',
                    'samochód': 'car',
                    'jestem': 'I am',
                    'jesteś': 'you are',
                    'on jest': 'he is',
                    'ona jest': 'she is',
                    'oni są': 'they are'
                },
                'ja': {
                    '皆': 'everyone',
                    'リラックス': 'relax',
                    'じゃがいも': 'potato',
                    'ジャガイモ': 'potatoes',
                    '映画': 'movie',
                    '面白い': 'funny',
                    'たくさん': 'a lot',
                    '私の友達': 'my friend',
                    'こんにちは': 'good afternoon',
                    '家': 'house',
                    '学校': 'school',
                    '子供': 'child',
                    '男': 'man',
                    '女': 'woman',
                    '仕事': 'work',
                    '車': 'car',
                    '私は': 'I am',
                    'あなたは': 'you are',
                    '彼は': 'he is',
                    '彼女は': 'she is',
                    '彼らは': 'they are'
                },
                'zh': {
                    '大家': 'everyone',
                    '放松': 'relax',
                    '马铃薯': 'potato',
                    '土豆': 'potatoes',
                    '电影': 'movie',
                    '有趣': 'funny',
                    '很多': 'a lot',
                    '我的朋友': 'my friend',
                    '下午好': 'good afternoon',
                    '房子': 'house',
                    '学校': 'school',
                    '孩子': 'child',
                    '男人': 'man',
                    '女人': 'woman',
                    '工作': 'work',
                    '汽车': 'car',
                    '我是': 'I am',
                    '你是': 'you are',
                    '他是': 'he is',
                    '她是': 'she is',
                    '他们是': 'they are'
                },
                'ko': {
                    '모두': 'everyone',
                    '휴식': 'relax',
                    '감자': 'potato',
                    '감자': 'potatoes',
                    '영화': 'movie',
                    '재미있는': 'funny',
                    '많은': 'a lot',
                    '내 친구': 'my friend',
                    '안녕하세요': 'good afternoon',
                    '집': 'house',
                    '학교': 'school',
                    '아이': 'child',
                    '남자': 'man',
                    '여자': 'woman',
                    '일': 'work',
                    '차': 'car',
                    '저는': 'I am',
                    '당신은': 'you are',
                    '그는': 'he is',
                    '그녀는': 'she is',
                    '그들은': 'they are'
                }
            }

            translator = Translator(to_lang=dest_lang, exceptions=exceptions.get(src_lang, {}))
            translation = translator.translate(src_text)
            self.dest_text_box.setPlainText(translation)

    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
