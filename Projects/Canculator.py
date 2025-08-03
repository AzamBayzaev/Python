import tkinter as tk
from tkinter import messagebox
import re


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.resizable(False, False)

        self.expression = ""
        self.last_result = None
        self._setup_ui()
        self._bind_keyboard()

    def _setup_ui(self):
        self.entry = tk.Entry(
            self.root, font=("Arial", 24), borderwidth=2,
            relief="ridge", justify="right"
        )
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="we")

        # Кнопки
        buttons = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('⌫', 1, 3), ('/', 1, 4),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3), ('√', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3), ('^', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3), ('%', 4, 4),
            ('±', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3, 2)
        ]

        for btn_info in buttons:
            text, row, col = btn_info[0], btn_info[1], btn_info[2]
            colspan = btn_info[3] if len(btn_info) > 3 else 1
            btn = tk.Button(
                self.root, text=text, font=("Arial", 18),
                command=lambda t=text: self.on_button_click(t),
                padx=10, pady=10
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)


        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

    def _bind_keyboard(self):
        self.root.bind('<Key>', self._on_key_press)

    def _on_key_press(self, event):
        key = event.char
        if key in '0123456789+-*/.()':
            self.on_button_click(key)
        elif key == '\r':
            self.on_button_click('=')
        elif key == '\x08':
            self.on_button_click('⌫')

    def _clear_display(self):
        self.entry.delete(0, tk.END)

    def _safe_eval(self, expr):

        sanitized = re.sub(r'[^\d+\-*/().√^%]', '', expr)

        sanitized = sanitized.replace('^', '**').replace('√', 'math.sqrt')

        sanitized = f'math.{sanitized}' if 'math.' in sanitized else sanitized
        try:
            return eval(sanitized, {'math': math, '__builtins__': None})
        except:
            return None

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self._clear_display()
        elif char == '⌫':
            self.expression = self.expression[:-1]
            self._clear_display()
            self.entry.insert(tk.END, self.expression)
        elif char == '±':
            if self.expression and self.expression[0] == '-':
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self._clear_display()
            self.entry.insert(tk.END, self.expression)
        elif char == '=':
            if not self.expression:
                return

            try:
                result = self._safe_eval(self.expression)
                if result is None:
                    raise ValueError("Invalid expression")

                self._clear_display()
                self.entry.insert(tk.END, str(result))
                self.last_result = result
                self.expression = str(result)
            except ZeroDivisionError:
                messagebox.showerror("Error", "Cannot divide by zero!")
                self.expression = ""
                self._clear_display()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid Expression: {str(e)}")
                self.expression = ""
                self._clear_display()
        else:
            self.expression += str(char)
            self._clear_display()
            self.entry.insert(tk.END, self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()