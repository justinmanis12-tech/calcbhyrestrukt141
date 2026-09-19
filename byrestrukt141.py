import tkinter as tk
from tkinter import font
import math
import re


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Инженерный Калькулятор PRO")
        self.root.geometry("450x650")
        self.root.resizable(False, False)

        self.bg_color = "#1E1E24"
        self.btn_bg_color = "#2B2D42"
        self.btn_fg_color = "#FFFFFF"
        self.btn_hover_color = "#3B3D52"
        self.btn_active_bg = "#4B4D62"
        self.operator_bg = "#EF233C"
        self.operator_fg = "#FFFFFF"
        self.clear_bg = "#D90429"
        self.equal_bg = "#8D99AE"
        self.display_bg = "#EDF2F4"
        self.display_fg = "#2B2D42"
        self.history_fg = "#8D99AE"

        self.root.configure(bg=self.bg_color)

        self.font_large = font.Font(family="Helvetica", size=24, weight="bold")
        self.font_medium = font.Font(family="Helvetica", size=16)
        self.font_small = font.Font(family="Helvetica", size=12)

        self.current_expression = ""
        self.history_expression = ""
        self.memory_value = 0.0
        self.result_displayed = False

        self._create_menu()
        self._create_display()
        self._create_buttons()
        self._bind_keys()

    def _create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Очистить историю", command=self.clear_history_log)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menubar)

    def _create_display(self):
        display_frame = tk.Frame(self.root, bg=self.bg_color)
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.memory_label = tk.Label(
            display_frame, text="", bg=self.bg_color, fg="#FFD166",
            font=self.font_small, anchor="w"
        )
        self.memory_label.pack(fill="x")

        self.history_label = tk.Label(
            display_frame, text=self.history_expression, bg=self.bg_color,
            fg=self.history_fg, font=self.font_medium, anchor="e"
        )
        self.history_label.pack(fill="x")

        self.display = tk.Entry(
            display_frame, font=self.font_large, bg=self.display_bg,
            fg=self.display_fg, borderwidth=0, justify="right"
        )
        self.display.pack(expand=True, fill="both", pady=5)
        self.display.insert(0, "0")
        self.display.config(state="readonly")

    def _create_buttons(self):
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(expand=True, fill="both", padx=5, pady=5)

        for i in range(5):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(8):
            buttons_frame.rowconfigure(i, weight=1)

        buttons = [
            ("MC", 0, 0, "mem"), ("MR", 0, 1, "mem"), ("M+", 0, 2, "mem"), ("M-", 0, 3, "mem"), ("MS", 0, 4, "mem"),
            ("sin", 1, 0, "sci"), ("cos", 1, 1, "sci"), ("tan", 1, 2, "sci"), ("deg", 1, 3, "sci"),
            ("rad", 1, 4, "sci"),
            ("log", 2, 0, "sci"), ("ln", 2, 1, "sci"), ("sqrt", 2, 2, "sci"), ("x^2", 2, 3, "sci"),
            ("x^y", 2, 4, "sci"),
            ("π", 3, 0, "sci"), ("e", 3, 1, "sci"), ("(", 3, 2, "sci"), (")", 3, 3, "sci"), ("n!", 3, 4, "sci"),
            ("C", 4, 0, "clear"), ("CE", 4, 1, "clear"), ("⌫", 4, 2, "clear"), ("/", 4, 3, "op"), ("%", 4, 4, "op"),
            ("7", 5, 0, "num"), ("8", 5, 1, "num"), ("9", 5, 2, "num"), ("*", 5, 3, "op"), ("1/x", 5, 4, "sci"),
            ("4", 6, 0, "num"), ("5", 6, 1, "num"), ("6", 6, 2, "num"), ("-", 6, 3, "op"), ("|x|", 6, 4, "sci"),
            ("1", 7, 0, "num"), ("2", 7, 1, "num"), ("3", 7, 2, "num"), ("+", 7, 3, "op"), ("10^x", 7, 4, "sci"),
            ("+/-", 8, 0, "num"), ("0", 8, 1, "num"), (".", 8, 2, "num"), ("=", 8, 3, "equal")
        ]

        for button in buttons:
            text, row, col, btn_type = button
            colspan = 2 if text == "=" else 1

            bg_col = self.btn_bg_color
            fg_col = self.btn_fg_color

            if btn_type == "num":
                bg_col = "#3a3c4f"
            elif btn_type == "op":
                bg_col = self.operator_bg
                fg_col = self.operator_fg
            elif btn_type == "clear":
                bg_col = self.clear_bg
            elif btn_type == "equal":
                bg_col = "#4CAF50"
            elif btn_type == "mem":
                bg_col = "#F4A261"
                fg_col = "#2B2D42"
            elif btn_type == "sci":
                bg_col = "#264653"

            btn = tk.Button(
                buttons_frame, text=text, bg=bg_col, fg=fg_col,
                font=self.font_medium, borderwidth=0,
                activebackground=self.btn_active_bg,
                activeforeground="#FFFFFF",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

            btn.bind("<Enter>", lambda e, b=btn, c=bg_col: self.on_enter(e, b, c))
            btn.bind("<Leave>", lambda e, b=btn, c=bg_col: self.on_leave(e, b, c))

    def on_enter(self, e, btn, original_bg):
        btn['background'] = self.btn_hover_color

    def on_leave(self, e, btn, original_bg):
        btn['background'] = original_bg

    def _bind_keys(self):
        self.root.bind("<Return>", lambda event: self.on_button_click("="))
        self.root.bind("<KP_Enter>", lambda event: self.on_button_click("="))
        self.root.bind("<BackSpace>", lambda event: self.on_button_click("⌫"))
        self.root.bind("<Escape>", lambda event: self.on_button_click("C"))

        keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '.', '+', '-', '*', '/', '(', ')', '%', '^']

        for key in keys:
            mapped_key = "x^y" if key == "^" else key
            self.root.bind(key, lambda event, char=mapped_key: self.on_button_click(char))

    def update_display(self, text):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.config(state="readonly")

    def update_history(self, text):
        self.history_label.config(text=text)

    def on_button_click(self, char):
        if self.display.get() == "Ошибка" or self.display.get() == "NaN":
            self.current_expression = ""
            self.update_display("0")

        if self.result_displayed and char.isdigit():
            self.current_expression = ""
            self.result_displayed = False
        else:
            self.result_displayed = False

        if char == "C":
            self.current_expression = ""
            self.update_display("0")
            self.update_history("")

        elif char == "CE":
            self.current_expression = ""
            self.update_display("0")

        elif char == "⌫":
            if len(self.current_expression) > 1:
                self.current_expression = self.current_expression[:-1]
                self.update_display(self.current_expression)
            else:
                self.current_expression = ""
                self.update_display("0")

        elif char == "=":
            self.calculate_result()

        elif char == "+/-":
            self.toggle_sign()

        elif char in ["MC", "MR", "M+", "M-", "MS"]:
            self.handle_memory(char)

        elif char in ["sin", "cos", "tan", "log", "ln", "sqrt", "n!", "1/x", "|x|", "10^x"]:
            self.apply_math_function(char)

        elif char == "x^2":
            self.current_expression += "**2"
            self.update_display(self.current_expression)

        elif char == "x^y":
            self.current_expression += "**"
            self.update_display(self.current_expression)

        elif char == "π":
            self.current_expression += str(math.pi)
            self.update_display(self.current_expression)

        elif char == "e":
            self.current_expression += str(math.e)
            self.update_display(self.current_expression)

        elif char in ["deg", "rad"]:
            self.apply_conversion(char)

        else:
            if self.current_expression == "0" and char.isdigit():
                self.current_expression = char
            else:
                self.current_expression += str(char)
            self.update_display(self.current_expression)

    def handle_memory(self, command):
        try:
            current_val = float(
                eval(self.format_expression(self.current_expression))) if self.current_expression else 0.0

            if command == "MC":
                self.memory_value = 0.0
                self.memory_label.config(text="")
            elif command == "MR":
                self.current_expression += str(self.memory_value)
                self.update_display(self.current_expression)
            elif command == "MS":
                self.memory_value = current_val
                self.memory_label.config(text="M")
            elif command == "M+":
                self.memory_value += current_val
                self.memory_label.config(text="M")
            elif command == "M-":
                self.memory_value -= current_val
                self.memory_label.config(text="M")
        except Exception:
            self.update_display("Ошибка")
            self.current_expression = ""

    def apply_math_function(self, func):
        try:
            expr = self.format_expression(self.current_expression)
            val = float(eval(expr)) if expr else 0.0

            result = 0.0

            if func == "sin":
                result = math.sin(math.radians(val))
            elif func == "cos":
                result = math.cos(math.radians(val))
            elif func == "tan":
                result = math.tan(math.radians(val))
            elif func == "log":
                if val <= 0: raise ValueError
                result = math.log10(val)
            elif func == "ln":
                if val <= 0: raise ValueError
                result = math.log(val)
            elif func == "sqrt":
                if val < 0: raise ValueError
                result = math.sqrt(val)
            elif func == "n!":
                if val < 0 or not val.is_integer(): raise ValueError
                result = math.factorial(int(val))
            elif func == "1/x":
                if val == 0: raise ZeroDivisionError
                result = 1 / val
            elif func == "|x|":
                result = abs(val)
            elif func == "10^x":
                result = 10 ** val

            result = round(result, 10)
            if result.is_integer():
                result = int(result)

            self.update_history(f"{func}({self.current_expression}) =")
            self.current_expression = str(result)
            self.update_display(self.current_expression)
            self.result_displayed = True

        except ValueError:
            self.update_display("Ош. значения")
            self.current_expression = ""
        except ZeroDivisionError:
            self.update_display("Деление на 0")
            self.current_expression = ""
        except Exception:
            self.update_display("Ошибка")
            self.current_expression = ""

    def apply_conversion(self, func):
        try:
            val = float(eval(self.format_expression(self.current_expression))) if self.current_expression else 0.0
            if func == "deg":
                res = math.degrees(val)
            elif func == "rad":
                res = math.radians(val)

            res = round(res, 10)
            if res.is_integer(): res = int(res)

            self.current_expression = str(res)
            self.update_display(self.current_expression)
            self.result_displayed = True
        except:
            self.update_display("Ошибка")

    def toggle_sign(self):
        if not self.current_expression:
            return

        try:
            pattern = r'(\-?\d+\.?\d*)$'
            match = re.search(pattern, self.current_expression)

            if match:
                last_number = match.group(1)
                if last_number.startswith('-'):
                    new_number = last_number[1:]
                else:
                    new_number = '-' + last_number

                self.current_expression = self.current_expression[:match.start()] + new_number
                self.update_display(self.current_expression)
        except Exception:
            pass

    def format_expression(self, expr):
        formatted = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
        formatted = formatted.replace('%', '/100')
        return formatted

    def calculate_result(self):
        if not self.current_expression:
            return

        try:
            expr = self.format_expression(self.current_expression)

            result = eval(expr, {"__builtins__": None}, {
                "math": math, "abs": abs, "sin": math.sin, "cos": math.cos,
                "tan": math.tan, "sqrt": math.sqrt
            })

            result = round(result, 10)
            if result.is_integer():
                result = int(result)

            self.update_history(f"{self.current_expression} =")

            self.current_expression = str(result)
            self.update_display(self.current_expression)
            self.result_displayed = True

        except ZeroDivisionError:
            self.update_history(self.current_expression + " =")
            self.update_display("Деление на 0")
            self.current_expression = ""
        except SyntaxError:
            self.update_display("Синтаксическая ошибка")
            self.current_expression = ""
        except Exception as e:
            self.update_display("Ошибка")
            self.current_expression = ""

    def clear_history_log(self):
        self.update_history("")

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("300x150")
        about_window.resizable(False, False)
        about_window.configure(bg=self.bg_color)

        lbl1 = tk.Label(about_window, text="Инженерный Калькулятор PRO", font=self.font_medium, bg=self.bg_color,
                        fg=self.btn_fg_color)
        lbl1.pack(pady=10)

        lbl2 = tk.Label(about_window, text="Разработано специально для тебя.\nПоддерживает мат. функции и память.",
                        bg=self.bg_color, fg=self.history_fg)
        lbl2.pack(pady=5)

        btn = tk.Button(about_window, text="Закрыть", command=about_window.destroy, bg=self.btn_bg_color,
                        fg=self.btn_fg_color)
        btn.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
