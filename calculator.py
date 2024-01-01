import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT = ("Arial", 24, "bold")
DEFAULT_FONT = ("Arial", 20)

CURRENT_RESULT_BACKGROUND = "#000000"
BACKGROUND_OPERATORS = "#292421"
DIGITS_COLOR = '#FFFFFF'
EQUAL_BUTTON_BACKGROUND = "#00CD66"
DIGITS_COLOR_BACKGROUND = "#292421"


class Calculator:
    def __init__(self):
        """root is current window."""
        self.root = tk.Tk()
        self.root.geometry("375x667")
        self.root.title("Calculator")
        self.root.resizable(True, True)
        self.root.iconbitmap("Calculator_image.ico")

        self.total_expression = ""
        self.current_expression = ""

        self.display_frame = self.main_frame()
        self.buttons_frame = self.buttons_frame()

        self.result_label, self.current_label = self.display_label()

        self.digits = {
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2),
            '.': (4, 3),
            "%": (4, 1)
        }
        self.operators = {
            "/": u"\u00F7",
            "*": "\u00D7",
            "-": "-",
            "+": "+"
        }

        self.buttons_frame.rowconfigure(0, weight=True)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=True)
            self.buttons_frame.columnconfigure(x, weight=True)

        self.digits_buttons()
        self.operator_buttons()
        self.special_buttons()

        self.bind_keyboard()
        self.backspace()

    def bind_keyboard(self):
        self.root.bind("<Return>", lambda x: self.evaluate())
        for key in self.digits:
            self.root.bind(str(key), lambda x, digit=key: self.add_expression(digit))

        for key in self.operators:
            self.root.bind(key, lambda x, operator=key: self.append_operator(operator))

    def backspace(self):
        self.root.bind('<BackSpace>', self.button_clear)

    def button_clear(self):
        self.current_expression = str(self.current_expression[:-1])
        self.update_current_label()

    def special_buttons(self):
        self.clean_button()
        self.equal_button()
        self.square_button()
        self.sqr_button()

    def main_frame(self):
        frame = tk.Frame(
            self.root,
            height=222,
            bg=CURRENT_RESULT_BACKGROUND
        )
        frame.pack(expand=True, fill="both")
        return frame

    def buttons_frame(self):
        frame = tk.Frame(
            self.root
        )
        frame.pack(expand=True, fill="both")
        return frame

    def add_expression(self, value):
        self.current_expression += str(value)
        self.update_current_label()

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_result_label()
        self.update_current_label()

    def digits_buttons(self):
        for digit, grid in self.digits.items():
            button = tk.Button(
                self.buttons_frame,
                text=str(digit),
                bg=DIGITS_COLOR_BACKGROUND,
                fg=DIGITS_COLOR,
                font=DIGITS_FONT,
                borderwidth=False,
                command=lambda x=digit: self.add_expression(x)
            )
            button.grid(row=grid[0], column=grid[1], sticky=tk.NSEW)

    def operator_buttons(self):
        index = 0
        for operator, symbol in self.operators.items():
            button = tk.Button(
                self.buttons_frame,
                text=symbol,
                bg=BACKGROUND_OPERATORS,
                fg=DIGITS_COLOR,
                font=DEFAULT_FONT,
                borderwidth=False,
                command=lambda x=operator: self.append_operator(x)
            )
            button.grid(row=index, column=4, sticky=tk.NSEW)
            index += 1

    def clean_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="C",
            bg=BACKGROUND_OPERATORS,
            fg=DIGITS_COLOR,
            font=DEFAULT_FONT,
            borderwidth=False,
            command=self.clean_data
        )
        button.grid(
            row=0,
            column=1,
            sticky=tk.NSEW,
        )

    def square(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}**2"))

        except (Exception,):
            self.current_expression = "Error"

        finally:
            self.update_current_label()

    def square_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="x\u00b2",
            bg=BACKGROUND_OPERATORS,
            fg=DIGITS_COLOR,
            font=DEFAULT_FONT,
            borderwidth=False,
            command=self.square
        )
        button.grid(
            row=0,
            column=2,
            sticky=tk.NSEW,
        )

    def sqr(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}**0.5"))

        except (Exception,):
            self.current_expression = "Error"

        finally:
            self.update_current_label()

    def sqr_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="\u221ax",
            bg=BACKGROUND_OPERATORS,
            fg=DIGITS_COLOR,
            font=DEFAULT_FONT,
            borderwidth=False,
            command=self.sqr
        )
        button.grid(
            row=0,
            column=3,
            sticky=tk.NSEW,
        )

    def equal_button(self):
        button = tk.Button(
            self.buttons_frame,
            text="=",
            bg=EQUAL_BUTTON_BACKGROUND,
            fg=DIGITS_COLOR,
            font=DEFAULT_FONT,
            borderwidth=False,
            command=self.evaluate
        )
        button.grid(
            row=4,
            column=4,
            sticky=tk.NSEW
        )

    def display_label(self):
        result_label = tk.Label(
            self.display_frame,
            text=self.total_expression,
            anchor=tk.E,
            bg=CURRENT_RESULT_BACKGROUND,
            fg=DIGITS_COLOR,
            padx=24,
            font=SMALL_FONT_STYLE
        )
        result_label.pack(expand=True, fill='both')

        current_label = tk.Label(
            self.display_frame,
            text=self.current_expression,
            anchor=tk.E,
            bg=CURRENT_RESULT_BACKGROUND,
            fg=DIGITS_COLOR,
            padx=24,
            font=LARGE_FONT_STYLE
        )
        current_label.pack(expand=True, fill='both')

        return result_label, current_label

    def update_result_label(self):
        expression = self.total_expression
        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.result_label.config(text=expression)

    def update_current_label(self):
        self.current_label.config(
            text=self.current_expression[:11]
        )

    def clean_data(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_current_label()
        self.update_result_label()

    def evaluate(self):
        try:
            symbol = self.total_expression[-1]
            for x in range(len(self.total_expression)):
                if self.total_expression[x] == "%":
                    result = float(self.total_expression[:x]) / 100
                    self.total_expression = str(result) + symbol

        except (Exception,):
            self.current_expression = "Error"

        try:
            for x in range(len(self.current_expression)):
                if self.current_expression[x] == "%":
                    result = float(self.current_expression[:x]) / 100
                    self.current_expression = str(result)

        except (Exception,):
            self.current_expression = "Error"

        self.total_expression += self.current_expression
        self.update_result_label()

        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""

        except (Exception,):
            self.current_expression = "Error"

        finally:
            self.update_current_label()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
