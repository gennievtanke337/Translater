from PyQt5 import QtWidgets, QtCore
from translate import Translator

class TranslatorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Перекладач')
        self.resize(800, 600)  # Встановлення розміру вікна

        # Layouts
        self.layout = QtWidgets.QVBoxLayout()

        # Source language selector
        self.src_lang_label = QtWidgets.QLabel('Мова оригіналу:')
        self.src_lang_combobox = QtWidgets.QComboBox()
        self.src_lang_combobox.addItems(['en', 'uk', 'ru', 'fr', 'de', 'es', 'it', 'pl'])
        self.src_lang_combobox.setCurrentText('en')
        self.layout.addWidget(self.src_lang_label)
        self.layout.addWidget(self.src_lang_combobox)

        # Destination language selector
        self.dest_lang_label = QtWidgets.QLabel('Мова перекладу:')
        self.dest_lang_combobox = QtWidgets.QComboBox()
        self.dest_lang_combobox.addItems(['en', 'uk', 'ru', 'fr', 'de', 'es', 'it', 'pl'])
        self.dest_lang_combobox.setCurrentText('uk')
        self.layout.addWidget(self.dest_lang_label)
        self.layout.addWidget(self.dest_lang_combobox)

        # Source text box
        self.src_text_label = QtWidgets.QLabel('Введіть текст:')
        self.src_text_box = QtWidgets.QTextEdit()
        self.src_text_box.setMinimumHeight(200)  # Встановлення мінімальної висоти текстового поля
        self.layout.addWidget(self.src_text_label)
        self.layout.addWidget(self.src_text_box)

        # Translate button
        self.translate_button = QtWidgets.QPushButton('Перекласти')
        self.translate_button.setMinimumHeight(50)  # Збільшення висоти кнопки
        self.translate_button.setStyleSheet("font-size: 18px;")  # Збільшення розміру шрифту кнопки
        self.translate_button.clicked.connect(self.translate_text)
        self.layout.addWidget(self.translate_button)

        # Destination text box
        self.dest_text_label = QtWidgets.QLabel('Переклад:')
        self.dest_text_box = QtWidgets.QTextEdit()
        self.dest_text_box.setMinimumHeight(200)  # Встановлення мінімальної висоти текстового поля
        self.dest_text_box.setReadOnly(True)
        self.layout.addWidget(self.dest_text_label)
        self.layout.addWidget(self.dest_text_box)

        # Збільшення розміру шрифту для всіх текстових полів та міток
        self.src_lang_label.setStyleSheet("font-size: 16px;")
        self.src_lang_combobox.setStyleSheet("font-size: 16px;")
        self.dest_lang_label.setStyleSheet("font-size: 16px;")
        self.dest_lang_combobox.setStyleSheet("font-size: 16px;")
        self.src_text_box.setStyleSheet("font-size: 16px;")
        self.dest_text_box.setStyleSheet("font-size: 16px;")
        self.src_text_label.setStyleSheet("font-size: 16px;")
        self.dest_text_label.setStyleSheet("font-size: 16px;")

        self.setLayout(self.layout)

    def translate_text(self):
        src_text = self.src_text_box.toPlainText().strip()
        src_lang = self.src_lang_combobox.currentText()
        dest_lang = self.dest_lang_combobox.currentText()

        if src_text:
            translator = Translator(from_lang=src_lang, to_lang=dest_lang)
            translation = translator.translate(src_text)
            self.dest_text_box.setPlainText(translation)
        else:
            self.dest_text_box.setPlainText("Введіть текст для перекладу")

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = TranslatorApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
