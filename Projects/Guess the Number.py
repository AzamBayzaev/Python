import tkinter as tk
from tkinter import messagebox
import random


class GuessNumberGame:
    MIN_NUMBER = 1
    MAX_NUMBER = 100
    DEFAULT_ATTEMPTS = 7

    def __init__(self, root):
        self.root = root
        self.root.title("Угадай число")
        self.root.resizable(False, False)

        self.reset_game()
        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        tk.Label(
            self.root,
            text=f"Угадай число от {self.MIN_NUMBER} до {self.MAX_NUMBER}",
            font=("Arial", 16)
        ).pack(pady=10)

        self.info_label = tk.Label(
            self.root,
            text=f"У вас {self.attempts_left} попыток",
            font=("Arial", 14)
        )
        self.info_label.pack(pady=5)


        self.entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            justify="center"
        )
        self.entry.pack(pady=5)
        self.entry.focus()


        self.guess_button = tk.Button(
            self.root,
            text="Угадать",
            font=("Arial", 14),
            command=self.check_guess
        )
        self.guess_button.pack(pady=5)

        self.reset_button = tk.Button(
            self.root,
            text="Начать заново",
            font=("Arial", 14),
            command=self.confirm_reset
        )
        self.reset_button.pack(pady=10)


        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14),
            fg="blue"
        )
        self.feedback_label.pack(pady=5)

    def bind_events(self):

        self.entry.bind('<Return>', lambda e: self.check_guess())

    def reset_game(self):

        self.number = random.randint(self.MIN_NUMBER, self.MAX_NUMBER)
        self.attempts_left = self.DEFAULT_ATTEMPTS
        self.feedback = ""
        self.update_ui(reset=True)

    def confirm_reset(self):

        if self.attempts_left < self.DEFAULT_ATTEMPTS:
            if messagebox.askyesno(
                    "Подтверждение",
                    "Вы уверены? Текущий прогресс будет потерян."
            ):
                self.reset_game()
        else:
            self.reset_game()

    def update_ui(self, reset=False):

        if reset:
            self.info_label.config(text=f"У вас {self.DEFAULT_ATTEMPTS} попыток")
            self.feedback_label.config(text="")
            self.entry.delete(0, tk.END)
            self.set_ui_state(True)
        else:
            self.info_label.config(text=f"Осталось попыток: {self.attempts_left}")
            self.feedback_label.config(text=self.feedback)

    def set_ui_state(self, enabled):

        state = tk.NORMAL if enabled else tk.DISABLED
        self.guess_button.config(state=state)
        self.entry.config(state=state)
        if enabled:
            self.entry.focus()

    def validate_input(self, guess_str):

        if not guess_str.isdigit():
            messagebox.showwarning(
                "Ошибка",
                "Пожалуйста, введите целое число."
            )
            return False

        guess = int(guess_str)
        if guess < self.MIN_NUMBER or guess > self.MAX_NUMBER:
            messagebox.showwarning(
                "Ошибка",
                f"Число должно быть от {self.MIN_NUMBER} до {self.MAX_NUMBER}."
            )
            return False

        return True

    def check_guess(self):

        guess_str = self.entry.get()

        if not self.validate_input(guess_str):
            return

        guess = int(guess_str)
        self.attempts_left -= 1

        if guess == self.number:
            self.feedback = f"Поздравляем! Вы угадали число {self.number}."
            self.feedback_label.config(fg="green")
            self.set_ui_state(False)
            messagebox.showinfo("Победа!", self.feedback)
        elif guess < self.number:
            self.feedback = "Слишком маленькое число."
            self.feedback_label.config(fg="blue")
        else:
            self.feedback = "Слишком большое число."
            self.feedback_label.config(fg="red")

        if self.attempts_left == 0 and guess != self.number:
            self.feedback = f"Попытки закончились! Загаданное число было {self.number}."
            self.feedback_label.config(fg="red")
            self.set_ui_state(False)
            messagebox.showinfo("Конец игры", self.feedback)

        self.update_ui()
        self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    game = GuessNumberGame(root)
    root.mainloop()