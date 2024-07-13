import tkinter as tk
from tkinter import ttk, messagebox
import requests

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перекладач")
        
        # Темна тема
        self.dark_mode = tk.BooleanVar()
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Використовуємо стандартну тему clam
        self.set_theme()

        # Мови
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
        ttk.Label(root, text="Введіть текст для перекладу:", style='Subtitle.TLabel').pack(pady=(20, 5))
        self.text_entry = ttk.Entry(root, width=50, font=('Arial', 12))
        self.text_entry.pack()
        
        ttk.Label(root, text="Мова оригіналу:", style='Subtitle.TLabel').pack(pady=(20, 5))
        self.origin_language = ttk.Combobox(root, values=list(self.languages.keys()), font=('Arial', 12))
        self.origin_language.pack()

        ttk.Label(root, text="Виберіть мову для перекладу:", style='Subtitle.TLabel').pack(pady=(20, 5))
        self.translation_language = ttk.Combobox(root, values=list(self.languages.keys()), font=('Arial', 12))
        self.translation_language.pack()

        self.translate_button = ttk.Button(root, text="Перекласти", command=self.translate_text, style='Accent.TButton')
        self.translate_button.pack(pady=20)
        
        self.translation_label = ttk.Label(root, text="", style='Result.TLabel', wraplength=400, anchor='center')
        self.translation_label.pack(pady=(20, 50))
        
        # Вибір теми
        ttk.Checkbutton(root, text="Темна тема", variable=self.dark_mode, command=self.set_theme).pack(pady=(10, 0))

        # Меню
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Повноекранний режим", command=self.toggle_fullscreen)
        view_menu.add_command(label="Вихід з повноекранного режиму", command=self.quit_fullscreen)

        # Встановлюємо початковий режим вікна
        self.fullscreen = False

        # Обробник клавіш Escape
        root.bind('<Escape>', lambda event: self.quit_fullscreen())

    def set_theme(self):
        theme = 'clam' if not self.dark_mode.get() else 'default'
        self.style.theme_use(theme)
        self.root.configure(bg=self.style.lookup(f'TButton.{theme}', 'background'))

    def translate_text(self):
        text = self.text_entry.get().strip()
        origin_lang = self.languages.get(self.origin_language.get())
        translation_lang = self.languages.get(self.translation_language.get())
        
        if text and origin_lang and translation_lang:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={origin_lang}&tl={translation_lang}&dt=t&q={text}"
            response = requests.get(url)
            
            if response.status_code == 200:
                translation = response.json()[0][0][0]
                self.translation_label.config(text=f"Перекладений текст:\n{translation}")
            else:
                messagebox.showerror("Помилка", "Не вдалося отримати переклад. Спробуйте ще раз пізніше.")
        else:
            messagebox.showwarning("Попередження", "Будь ласка, введіть текст і виберіть мови.")

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
