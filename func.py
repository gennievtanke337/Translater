import tkinter as tk
from tkinter import ttk, messagebox
import requests

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перекладач")
        
        # Теми
        self.themes = ['clam', 'alt', 'default', 'classic', 'vista']
        self.current_theme = tk.StringVar(value=self.themes[0])

        # Мови інтерфейсу
        self.interface_languages = {
            'Українська': 'uk',
            'Англійська': 'en'
        }
        self.current_language = tk.StringVar(value='uk')
        self.texts = self.get_texts('uk')
        
        # Темна тема
        self.dark_mode = tk.BooleanVar()
        self.style = ttk.Style()
        self.style.theme_use(self.current_theme.get())
        self.set_theme()

        # Мови перекладу
        self.languages = {
            'Англійська': 'en',
            'Іспанська': 'es',
            'Французька': 'fr',
            'Німецька': 'de',
            'Китайська (спрощена)': 'zh-CN',
            'Японська': 'ja',
            'Російська': 'ru',
            'Арабська': 'ar',
            'Гінді': 'hi',
            'Українська': 'uk',
            'Португальська': 'pt',
        }
        
        # Віджети
        self.create_widgets()
        
        # Обробник клавіш Escape
        root.bind('<Escape>', lambda event: self.quit_fullscreen())

    def get_texts(self, lang):
        texts = {
            'uk': {
                'title': "Перекладач",
                'input_label': "Введіть текст для перекладу:",
                'origin_language_label': "Мова оригіналу:",
                'translation_language_label': "Виберіть мову для перекладу:",
                'translate_button': "Перекласти",
                'dark_mode': "Темна тема",
                'settings': "Налаштування",
                'fullscreen': "Повноекранний режим",
                'exit_fullscreen': "Вихід з повноекранного режиму",
                'theme_label': "Виберіть тему:",
                'language_label': "Виберіть мову інтерфейсу:",
                'translated_text': "Перекладений текст:",
                'error': "Помилка",
                'warning': "Попередження",
                'error_message': "Не вдалося отримати переклад. Спробуйте ще раз пізніше.",
                'warning_message': "Будь ласка, введіть текст і виберіть мови."
            },
            'en': {
                'title': "Translator",
                'input_label': "Enter text to translate:",
                'origin_language_label': "Source language:",
                'translation_language_label': "Select target language:",
                'translate_button': "Translate",
                'dark_mode': "Dark mode",
                'settings': "Settings",
                'fullscreen': "Fullscreen mode",
                'exit_fullscreen': "Exit fullscreen mode",
                'theme_label': "Select theme:",
                'language_label': "Select interface language:",
                'translated_text': "Translated text:",
                'error': "Error",
                'warning': "Warning",
                'error_message': "Failed to get translation. Please try again later.",
                'warning_message': "Please enter text and select languages."
            }
        }
        return texts[lang]

    def create_widgets(self):
        self.input_label = ttk.Label(self.root, text=self.texts['input_label'], style='Subtitle.TLabel')
        self.input_label.pack(pady=(20, 5))
        
        self.text_entry = ttk.Entry(self.root, width=50, font=('Arial', 12))
        self.text_entry.pack()
        self.text_entry.bind('<Return>', self.translate_text)

        self.origin_language_label = ttk.Label(self.root, text=self.texts['origin_language_label'], style='Subtitle.TLabel')
        self.origin_language_label.pack(pady=(20, 5))
        
        self.origin_language = ttk.Combobox(self.root, values=list(self.languages.keys()), font=('Arial', 12))
        self.origin_language.pack()

        self.translation_language_label = ttk.Label(self.root, text=self.texts['translation_language_label'], style='Subtitle.TLabel')
        self.translation_language_label.pack(pady=(20, 5))
        
        self.translation_language = ttk.Combobox(self.root, values=list(self.languages.keys()), font=('Arial', 12))
        self.translation_language.pack()

        self.translate_button = ttk.Button(self.root, text=self.texts['translate_button'], command=self.translate_text, style='Accent.TButton')
        self.translate_button.pack(pady=20)
        
        self.translation_label = ttk.Label(self.root, text="", style='Result.TLabel', wraplength=400, anchor='center')
        self.translation_label.pack(pady=(20, 50))
        
        self.dark_mode_checkbutton = ttk.Checkbutton(self.root, text=self.texts['dark_mode'], variable=self.dark_mode, command=self.set_theme)
        self.dark_mode_checkbutton.pack(pady=(10, 0))

        # Меню
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.texts['settings'], menu=self.view_menu)
        self.view_menu.add_command(label=self.texts['fullscreen'], command=self.toggle_fullscreen)
        self.view_menu.add_command(label=self.texts['exit_fullscreen'], command=self.quit_fullscreen)
        
        self.settings_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label=self.texts['settings'], menu=self.settings_menu)
        
        self.theme_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=self.texts['theme_label'], menu=self.theme_menu)
        for theme in self.themes:
            self.theme_menu.add_radiobutton(label=theme, variable=self.current_theme, value=theme, command=self.set_theme)

        self.language_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=self.texts['language_label'], menu=self.language_menu)
        for lang in self.interface_languages:
            self.language_menu.add_radiobutton(label=lang, variable=self.current_language, value=self.interface_languages[lang], command=self.change_language)

    def set_theme(self):
        self.style.theme_use(self.current_theme.get())
        self.root.configure(bg=self.style.lookup(f'TButton.{self.current_theme.get()}', 'background'))

    def change_language(self):
        self.texts = self.get_texts(self.current_language.get())
        self.update_texts()

    def update_texts(self):
        self.root.title(self.texts['title'])
        self.input_label.config(text=self.texts['input_label'])
        self.origin_language_label.config(text=self.texts['origin_language_label'])
        self.translation_language_label.config(text=self.texts['translation_language_label'])
        self.translate_button.config(text=self.texts['translate_button'])
        self.dark_mode_checkbutton.config(text=self.texts['dark_mode'])
        
        self.menubar.entryconfig(1, label=self.texts['settings'])
        self.view_menu.entryconfig(0, label=self.texts['fullscreen'])
        self.view_menu.entryconfig(1, label=self.texts['exit_fullscreen'])
        
        self.settings_menu.entryconfig(0, label=self.texts['theme_label'])
        self.settings_menu.entryconfig(1, label=self.texts['language_label'])

    def translate_text(self, event=None):
        text = self.text_entry.get().strip()
        origin_lang = self.languages.get(self.origin_language.get())
        translation_lang = self.languages.get(self.translation_language.get())
        
        if text and origin_lang and translation_lang:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={origin_lang}&tl={translation_lang}&dt=t&q={text}"
            response = requests.get(url)
            
            if response.status_code == 200:
                translation = response.json()[0][0][0]
                self.translation_label.config(text=f"{self.texts['translated_text']}\n{translation}")
            else:
                messagebox.showerror(self.texts['error'], self.texts['error_message'])
        else:
            messagebox.showwarning(self.texts['warning'], self.texts['warning_message'])

    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', True)
        self.fullscreen = True

    def quit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        self.fullscreen = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
