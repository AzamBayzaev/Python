import tkinter as tk
from tkinter import messagebox
import random
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict


class TicTacToe:
    # Константы для стилей и настроек
    STYLES = {
        "font_small": ("Arial", 14),
        "font_large": ("Arial", 32),
        "colors": {
            "X": "red",
            "O": "blue",
            "bg_winner": "lightgreen",
            "bg_default": "SystemButtonFace"
        }
    }

    DIFFICULTY_SETTINGS = {
        "easy": {"smart_move_prob": 0.0},
        "medium": {"smart_move_prob": 0.7},
        "hard": {"smart_move_prob": 1.0}
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Крестики-нолики")

        # Инициализация состояния игры
        self.game_active = True
        self.game_mode = "single"  # 'single' или 'multiplayer'
        self.difficulty = "easy"  # 'easy', 'medium', 'hard'
        self.scores = {"X": 0, "O": 0}
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.load_scores()
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self) -> None:
        """Создает все элементы интерфейса"""
        # Меню
        self.create_menu()

        # Фрейм для счета и информации о ходе
        self.score_frame = tk.Frame(self.root)
        self.score_frame.grid(row=0, column=0, columnspan=3, pady=10)

        self.score_label = tk.Label(
            self.score_frame,
            text="X: 0 | O: 0",
            font=self.STYLES["font_small"]
        )
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.current_player_label = tk.Label(
            self.score_frame,
            text="",
            font=self.STYLES["font_small"]
        )
        self.current_player_label.pack(side=tk.LEFT, padx=10)

        # Игровое поле
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    font=self.STYLES["font_large"],
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                btn.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        # Кнопка сброса
        self.reset_button = tk.Button(
            self.root,
            text="Новая игра",
            font=self.STYLES["font_small"],
            command=self.reset_board
        )
        self.reset_button.grid(row=4, column=0, columnspan=3, pady=10)

    def create_menu(self) -> None:
        """Создает меню приложения"""
        menubar = tk.Menu(self.root)

        # Меню игры
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Новая игра", command=self.reset_board)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Игра", menu=game_menu)

        # Меню режима игры
        mode_var = tk.StringVar(value=self.game_mode)
        mode_menu = tk.Menu(menubar, tearoff=0)
        mode_menu.add_radiobutton(
            label="Одиночная игра",
            variable=mode_var,
            command=lambda: self.set_game_mode("single")
        )
        mode_menu.add_radiobutton(
            label="Два игрока",
            variable=mode_var,
            command=lambda: self.set_game_mode("multiplayer")
        )
        menubar.add_cascade(label="Режим", menu=mode_menu)

        # Меню сложности
        diff_var = tk.StringVar(value=self.difficulty)
        difficulty_menu = tk.Menu(menubar, tearoff=0)
        difficulty_menu.add_radiobutton(
            label="Легкая",
            variable=diff_var,
            command=lambda: self.set_difficulty("easy")
        )
        difficulty_menu.add_radiobutton(
            label="Средняя",
            variable=diff_var,
            command=lambda: self.set_difficulty("medium")
        )
        difficulty_menu.add_radiobutton(
            label="Сложная",
            variable=diff_var,
            command=lambda: self.set_difficulty("hard")
        )
        menubar.add_cascade(label="Сложность", menu=difficulty_menu)

        self.root.config(menu=menubar)

    def set_game_mode(self, mode: str) -> None:
        """Устанавливает режим игры"""
        self.game_mode = mode
        self.reset_board()

    def set_difficulty(self, difficulty: str) -> None:
        """Устанавливает уровень сложности"""
        self.difficulty = difficulty
        if self.game_mode == "single" and self.current_player == "O" and self.game_active:
            self.root.after(500, self.computer_move)

    def start_new_game(self) -> None:
        """Начинает новую игру"""
        self.current_player = random.choice(["X", "O"])
        self.update_current_player_label()
        if self.game_mode == "single" and self.current_player == "O":
            self.root.after(500, self.computer_move)

    def make_move(self, row: int, col: int) -> None:
        """Обрабатывает ход игрока"""
        if not self.game_active:
            return
        if self.board[row][col] != "":
            return
        if self.game_mode == "single" and self.current_player == "O":
            return

        self.place_symbol(row, col)

    def place_symbol(self, row: int, col: int) -> None:
        """Размещает символ на поле и проверяет условия окончания игры"""
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            fg=self.STYLES["colors"][self.current_player]
        )

        if win_cells := self.check_winner(self.current_player):
            self.handle_win(win_cells)
        elif self.is_board_full():
            self.handle_draw()
        else:
            self.switch_player()
            if self.game_mode == "single" and self.current_player == "O" and self.game_active:
                self.root.after(500, self.computer_move)

    def handle_win(self, win_cells: List[Tuple[int, int]]) -> None:
        """Обрабатывает победу"""
        self.highlight_winner(win_cells)
        self.scores[self.current_player] += 1
        self.save_scores()
        self.update_score()
        self.game_active = False
        messagebox.showinfo("Игра окончена", f"Победил {self.current_player}!")
        self.root.after(2000, self.reset_board)

    def handle_draw(self) -> None:
        """Обрабатывает ничью"""
        self.game_active = False
        messagebox.showinfo("Игра окончена", "Ничья!")
        self.root.after(1000, self.reset_board)

    def switch_player(self) -> None:
        """Меняет текущего игрока"""
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_current_player_label()

    def update_current_player_label(self) -> None:
        """Обновляет метку с текущим игроком"""
        player_text = f"Ход: {self.current_player}"
        if self.game_mode == "single" and self.current_player == "O":
            player_text += " (Компьютер)"
        self.current_player_label.config(text=player_text)

    def computer_move(self) -> None:
        """Выполняет ход компьютера"""
        if not self.game_active:
            return

        smart_prob = self.DIFFICULTY_SETTINGS[self.difficulty]["smart_move_prob"]
        if random.random() < smart_prob:
            self.computer_move_smart()
        else:
            self.computer_move_random()

    def computer_move_random(self) -> None:
        """Случайный ход компьютера"""
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.place_symbol(row, col)

    def computer_move_smart(self) -> None:
        """Умный ход компьютера"""
        # Проверка на выигрышный ход
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        self.board[i][j] = ""
                        self.place_symbol(i, j)
                        return
                    self.board[i][j] = ""

        # Блокировка игрока
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = ""
                        self.place_symbol(i, j)
                        return
                    self.board[i][j] = ""

        # Стратегические позиции
        if self.board[1][1] == "":  # Центр
            self.place_symbol(1, 1)
            return

        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for i, j in corners:
            if self.board[i][j] == "":
                self.place_symbol(i, j)
                return

        # Если ничего не найдено - случайный ход
        self.computer_move_random()

    def check_winner(self, player: str) -> Optional[List[Tuple[int, int]]]:
        """Проверяет, есть ли победитель"""
        # Проверка строк и столбцов
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return [(i, j) for j in range(3)]
            if all(self.board[j][i] == player for j in range(3)):
                return [(j, i) for j in range(3)]

        # Проверка диагоналей
        if all(self.board[i][i] == player for i in range(3)):
            return [(i, i) for i in range(3)]
        if all(self.board[i][2 - i] == player for i in range(3)):
            return [(i, 2 - i) for i in range(3)]

        return None

    def is_board_full(self) -> bool:
        """Проверяет, заполнено ли поле"""
        return all(cell != "" for row in self.board for cell in row)

    def highlight_winner(self, cells: List[Tuple[int, int]]) -> None:
        """Подсвечивает выигрышную комбинацию"""
        for r, c in cells:
            self.buttons[r][c].config(bg=self.STYLES["colors"]["bg_winner"])

    def reset_board(self) -> None:
        """Сбрасывает игровое поле"""
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text="",
                    bg=self.STYLES["colors"]["bg_default"],
                    fg="black"
                )
        self.game_active = True
        self.start_new_game()
        self.update_score()

    def load_scores(self) -> None:
        """Загружает сохраненные результаты"""
        try:
            scores_file = Path("scores.json")
            if scores_file.exists():
                with open(scores_file, "r") as f:
                    self.scores = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.scores = {"X": 0, "O": 0}

    def save_scores(self) -> None:
        """Сохраняет результаты игры"""
        try:
            with open("scores.json", "w") as f:
                json.dump(self.scores, f)
        except IOError:
            pass

    def update_score(self) -> None:
        """Обновляет отображение счета"""
        self.score_label.config(text=f"X: {self.scores['X']} | O: {self.scores['O']}")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)


    def on_closing():
        game.save_scores()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()