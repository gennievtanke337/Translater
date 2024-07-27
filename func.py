import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import requests

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перекладач")

        # Тема
        self.themes = ['clam', 'alt', 'default', 'classic', 'vista', 'xpnative']
        self.current_theme = tk.StringVar(value=self.themes[0])

        # Мови інтерфейсу
        self.interface_languages = {
            'Українська': 'uk',
            'English': 'en'
        }
        self.current_language = tk.StringVar(value='uk')
        self.texts = self.get_texts('uk')

        # Стиль
        self.style = ttk.Style()
        self.style.theme_use(self.current_theme.get())

        # Мови перекладу
        self.languages = {
            'Українська': 'uk',
            'Англійська': 'en',
            'Іспанська': 'es',
            'Французька': 'fr',
            'Німецька': 'de',
            'Китайська (спрощена)': 'zh-CN',
            'Японська': 'ja',
            'Російська': 'ru',
            'Арабська': 'ar',
            'Гінді': 'hi',
            'Португальська': 'pt',
        }

        # Віджети
        self.create_widgets()

        # Обробник клавіш Escape
        root.bind('<Escape>', lambda event: self.quit_fullscreen())

        # Вибрати вкладку перекладу при запуску
        self.notebook.select(self.translation_tab)

    def get_texts(self, lang):
        texts = {
            'uk': {
                'title': "Перекладач",
                'input_label': "Введіть текст для перекладу:",
                'origin_language_label': "Мова оригіналу:",
                'translation_language_label': "Виберіть мову для перекладу:",
                'translate_button': "Перекласти",
                'settings': "Налаштування",
                'fullscreen': "Повноекранний режим",
                'exit_fullscreen': "Вихід з повноекранного режиму",
                'theme_label': "Виберіть тему:",
                'language_label': "Виберіть мову інтерфейсу:",
                'background_label': "Виберіть фон:",
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
                'settings': "Settings",
                'fullscreen': "Fullscreen mode",
                'exit_fullscreen': "Exit fullscreen mode",
                'theme_label': "Select theme:",
                'language_label': "Select interface language:",
                'background_label': "Select background:",
                'translated_text': "Translated text:",
                'error': "Error",
                'warning': "Warning",
                'error_message': "Failed to get translation. Please try again later.",
                'warning_message': "Please enter text and select languages."
            }
        }
        return texts[lang]

    def create_widgets(self):
        # Створення Canvas для фону
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Створення фону
        self.bg_image = None
        self.bg_image_id = None

        # Створення фреймів
        self.main_frame = ttk.Frame(self.canvas, padding=10)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Створення вкладок
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text=self.texts['settings'])

        self.translation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.translation_tab, text="Переклад")

        self.create_translation_widgets()
        self.create_settings_widgets()

    def create_translation_widgets(self):
        # Елементи для перекладу
        self.input_label = ttk.Label(self.translation_tab, text=self.texts['input_label'], font=('Arial', 12, 'bold'))
        self.input_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky='w')

        self.text_entry = ttk.Entry(self.translation_tab, width=50, font=('Arial', 12))
        self.text_entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.text_entry.bind('<Return>', self.translate_text)

        self.origin_language_label = ttk.Label(self.translation_tab, text=self.texts['origin_language_label'], font=('Arial', 12, 'bold'))
        self.origin_language_label.grid(row=2, column=0, pady=(10, 5), sticky='w')

        self.origin_language = ttk.Combobox(self.translation_tab, values=list(self.languages.keys()), font=('Arial', 12))
        self.origin_language.grid(row=2, column=1, pady=(10, 5))

        self.translation_language_label = ttk.Label(self.translation_tab, text=self.texts['translation_language_label'], font=('Arial', 12, 'bold'))
        self.translation_language_label.grid(row=3, column=0, pady=(10, 5), sticky='w')

        self.translation_language = ttk.Combobox(self.translation_tab, values=list(self.languages.keys()), font=('Arial', 12))
        self.translation_language.grid(row=3, column=1, pady=(10, 5))

        self.translate_button = ttk.Button(self.translation_tab, text=self.texts['translate_button'], command=self.translate_text)
        self.translate_button.grid(row=4, column=0, columnspan=2, pady=15)

        self.translation_label = ttk.Label(self.translation_tab, text="", wraplength=self.canvas.winfo_width() - 60, anchor='center', font=('Arial', 12, 'italic'))
        self.translation_label.grid(row=5, column=0, columnspan=2, pady=(15, 20))

    def create_settings_widgets(self):
        # Елементи для налаштувань
        self.theme_label = ttk.Label(self.settings_tab, text=self.texts['theme_label'], font=('Arial', 12, 'bold'))
        self.theme_label.grid(row=0, column=0, pady=(10, 5), sticky='w')

        self.theme_combobox = ttk.Combobox(self.settings_tab, values=self.themes, textvariable=self.current_theme, font=('Arial', 12))
        self.theme_combobox.grid(row=0, column=1, pady=(10, 5))
        self.theme_combobox.bind('<<ComboboxSelected>>', lambda e: self.set_theme())

        self.language_label = ttk.Label(self.settings_tab, text=self.texts['language_label'], font=('Arial', 12, 'bold'))
        self.language_label.grid(row=1, column=0, pady=(10, 5), sticky='w')

        self.language_combobox = ttk.Combobox(self.settings_tab, values=list(self.interface_languages.keys()), textvariable=self.current_language, font=('Arial', 12))
        self.language_combobox.grid(row=1, column=1, pady=(10, 5))
        self.language_combobox.bind('<<ComboboxSelected>>', lambda e: self.change_language())

        self.background_button = ttk.Button(self.settings_tab, text=self.texts['background_label'], command=self.set_background)
        self.background_button.grid(row=2, column=0, columnspan=2, pady=(10, 5))

        # Видалено комбобокс для роздільної здатності

    def set_theme(self):
        self.style.theme_use(self.current_theme.get())
        self.canvas.config(bg=self.style.lookup(f'TButton.{self.current_theme.get()}', 'background'))

    def change_language(self):
        lang_code = self.interface_languages[self.current_language.get()]
        self.texts = self.get_texts(lang_code)
        self.update_texts()
        self.update_language_comboboxes()

    def update_texts(self):
        self.root.title(self.texts['title'])
        self.input_label.config(text=self.texts['input_label'])
        self.origin_language_label.config(text=self.texts['origin_language_label'])
        self.translation_language_label.config(text=self.texts['translation_language_label'])
        self.translate_button.config(text=self.texts['translate_button'])
        self.background_button.config(text=self.texts['background_label'])
        self.theme_label.config(text=self.texts['theme_label'])
        self.language_label.config(text=self.texts['language_label'])

        self.notebook.tab(0, text=self.texts['settings'])
        self.notebook.tab(1, text=self.texts['title'])

    def update_language_comboboxes(self):
        # Оновлення назв мов у комбобоксах
        if self.current_language.get() == 'English':
            self.languages = {
                'Ukrainian': 'uk',
                'English': 'en',
                'Spanish': 'es',
                'French': 'fr',
                'German': 'de',
                'Chinese (Simplified)': 'zh-CN',
                'Japanese': 'ja',
                'Russian': 'ru',
                'Arabic': 'ar',
                'Hindi': 'hi',
                'Portuguese': 'pt',
            }
        else:
            self.languages = {
                'Українська': 'uk',
                'Англійська': 'en',
                'Іспанська': 'es',
                'Французька': 'fr',
                'Німецька': 'de',
                'Китайська (спрощена)': 'zh-CN',
                'Японська': 'ja',
                'Російська': 'ru',
                'Арабська': 'ar',
                'Гінді': 'hi',
                'Португальська': 'pt',
            }

        self.origin_language.config(values=list(self.languages.keys()))
        self.translation_language.config(values=list(self.languages.keys()))

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

    def set_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            
            if self.bg_image_id:
                self.canvas.delete(self.bg_image_id)
                
            self.bg_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
            self.canvas.lower(self.bg_image_id)  # Ensure background is below other widgets

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
