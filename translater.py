from PyQt5 import QtWidgets, QtCore, QtGui
from googletrans import Translator, LANGUAGES

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
        self.dest_lang_label = QtWidgets.QLabel('Мова перекладу:')
        self.dest_lang_combobox = QtWidgets.QComboBox()

        for lang in LANGUAGES.values():
            self.src_lang_combobox.addItem(lang, lang)
            self.dest_lang_combobox.addItem(lang, lang)

        self.layout.addWidget(self.src_lang_label)
        self.layout.addWidget(self.src_lang_combobox)
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
            translator = Translator()
            translation = translator.translate(src_text, src=src_lang, dest=dest_lang).text
            self.dest_text_box.setPlainText(translation)

    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
