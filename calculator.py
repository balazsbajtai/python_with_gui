from tkinter import *


class Calculator:
    """
    Calculator class that holds functions for calculating arithmetic operations.
    """
    def __init__(self):
        self.current = ''
        self.sign = 1

    def calculate(self, operation_str):
        """Calculates arithmetic operations based on a string input.

        :param operation_str: calculation as a string
        :return: result as float
        """
        result = 0
        bracket_open = False
        bracket_operation = []
        multiply_divide_flag = False
        queue = []  # FIFO
        self.current = ''
        self.sign = 1

        for i in range(len(operation_str)):
            sstr = operation_str[i]

            if sstr in ['*', '/']:
                if bracket_open:
                    bracket_operation.append(float(self.current))
                    bracket_operation.append(sstr)
                    self.current = ''
                else:
                    queue.append(float(self.current))
                    queue.append(sstr)
                    self.current = ''
                    multiply_divide_flag = True

            elif sstr in ['-', '+']:
                if self.current:
                    if bracket_open:
                        bracket_operation.append(float(self.current))
                        bracket_operation.append(sstr)
                        self.current = ''
                    elif multiply_divide_flag:
                        queue.append(float(self.current))
                        result += self.calculate_multiplication_division(queue)
                        multiply_divide_flag = False
                    else:
                        result += float(self.current) * self.sign

                if sstr == '-':
                    self.sign = -1
                else:
                    self.sign = 1
                self.current = ''

            elif sstr == '(':
                bracket_open = True

            elif sstr == ')':
                bracket_open = False
                bracket_operation.append(float(self.current))
                op_str = ''.join([str(x) for x in bracket_operation])
                bracket_operation.clear()
                self.current = self.calculate(op_str)
                self.sign = 1

            else:
                self.current += sstr

        if multiply_divide_flag:
            queue.append(float(self.current))
            result += self.calculate_multiplication_division(queue)

        if self.current:
            return result + float(self.current) * self.sign
        else:
            return result

    def calculate_multiplication_division(self, queue):
        """Calculates multiplication and division based on a queue input.

        :param queue: calculation as a queue
        :return: result as float
        """
        self.current = ''

        if len(queue) == 3:
            first = queue.pop(0)
            op_sign = queue.pop(0)
            second = queue.pop(0)
            if op_sign == '*':
                return float(first) * float(second) * self.sign
            else:
                return float(first) / float(second) * self.sign
        else:
            current_queue = [queue.pop(0) for x in range(3)]
            operation_result = self.calculate_multiplication_division(current_queue)
            queue.insert(0, operation_result)

            while queue:
                current_queue = [queue.pop(0) for x in range(3)]
                operation_result = self.calculate_multiplication_division(current_queue)
                if len(queue):
                    queue.insert(0, operation_result)

            return operation_result * self.sign


class CalculatorGUI:
    """
    CalculatorGUI class that holds functions for setting up a user interface for a calculator.
    """
    def __init__(self):
        self.root = Tk()
        self.root.title('Calculator')
        self.root.geometry("300x300")
        self.root.maxsize(300, 300)
        self.root.minsize(300, 300)
        self.var = StringVar()
        self.var_tracker = StringVar()
        self.calc_done = False

        canvas = Canvas(self.root, height=300, width=300, bg='grey')
        canvas.pack()

        main_frame = Frame(canvas, bg='white')
        main_frame.place(relwidth=0.96, relheight=0.96, relx=0.02, rely=0.02)

        top_frame = Frame(main_frame, bg='white')
        buttons_frame = Frame(main_frame, bg='white')

        op_tracker = Label(top_frame, textvariable=self.var_tracker, anchor=E, font=("Arial", 11), pady=5)
        op_tracker.pack(fill='x')
        result_label = Label(top_frame, textvariable=self.var, anchor=E, font=("Arial", 22), pady=5)
        result_label.pack(fill='x')

        self.create_buttons_frame(buttons_frame)

        top_frame.place(relwidth=0.98, relheight=0.3, relx=0.01, rely=0.01)
        buttons_frame.place(relwidth=0.98, relheight=0.7, relx=0.01, rely=0.29)

        self.root.mainloop()

    def clear_screen(self):
        self.var.set('')
        self.var_tracker.set('')

    def number_btn_click(self, number):
        if self.calc_done:
            self.clear_screen()
            self.calc_done = False
        self.var.set(self.var.get() + str(number))
        self.var_tracker.set(self.var_tracker.get() + str(number))

    def other_btn_click(self, text):
        if self.calc_done:
            self.clear_screen()
            self.calc_done = False
        self.var.set('')
        self.var_tracker.set(self.var_tracker.get() + f' {text} ')

    def equals_btn_click(self):
        operation_str = self.var_tracker.get().replace(' ', '')
        if '(' in operation_str and ')' not in operation_str:
            operation_str += ')'
            self.var_tracker.set(self.var_tracker.get() + ') =')
        elif ')' in operation_str and '(' not in operation_str:
            operation_str = operation_str.replace(')', '')
            self.var_tracker.set(self.var_tracker.get().replace(')', '') + ' =')
        else:
            self.var_tracker.set(self.var_tracker.get() + ' =')

        try:
            calculator = Calculator()
            result = calculator.calculate(operation_str)
            self.var.set(result)
        except BaseException:
            self.var.set('Invalid syntax')
        self.calc_done = True

    def del_btn_click(self):
        current_var = self.var.get()
        self.var.set(current_var[:-1])
        current_var_tracker = self.var_tracker.get()
        self.var_tracker.set(current_var_tracker[:-1])

    def dot_btn_click(self):
        self.var.set(self.var.get() + '.')
        self.var_tracker.set(self.var_tracker.get() + '.')

    def open_bracket_btn_click(self):
        self.var.set(self.var.get() + '(')
        self.var_tracker.set(self.var_tracker.get() + '(')

    def close_bracket_btn_click(self):
        self.var.set(self.var.get() + ')')
        self.var_tracker.set(self.var_tracker.get() + ')')

    def create_num_btn(self, number, x, y, frame):
        btn = Button(frame, text=str(number), bd=0, relief=RAISED, bg='lightgrey',
                     command=lambda: self.number_btn_click(number))
        btn.grid(row=x, column=y, padx=1, pady=1, sticky="NSEW")
        return btn

    def create_other_btn(self, text, x, y, frame):
        btn = Button(frame, text=str(text), bd=0, relief=RAISED, bg='lightgrey',
                     command=lambda: self.other_btn_click(text))
        btn.grid(row=x, column=y, padx=1, pady=1, sticky="NSEW")
        return btn

    def create_buttons_frame(self, buttons_frame):
        Grid.rowconfigure(buttons_frame, 0, weight=1)
        Grid.rowconfigure(buttons_frame, 1, weight=1)
        Grid.rowconfigure(buttons_frame, 2, weight=1)
        Grid.rowconfigure(buttons_frame, 3, weight=1)
        Grid.rowconfigure(buttons_frame, 4, weight=1)
        Grid.columnconfigure(buttons_frame, 0, weight=1)
        Grid.columnconfigure(buttons_frame, 1, weight=1)
        Grid.columnconfigure(buttons_frame, 2, weight=1)
        Grid.columnconfigure(buttons_frame, 3, weight=1)

        btn_clear = Button(buttons_frame, text='C', bd=0, command=self.clear_screen)
        btn_clear.grid(row=0, column=0, padx=1, pady=1, sticky="NSEW")
        btn_multiply = self.create_other_btn('*', 0, 1, buttons_frame)
        btn_divide = self.create_other_btn('/', 0, 2, buttons_frame)
        btn_del = Button(buttons_frame, text='<', bd=0, command=self.del_btn_click)
        btn_del.grid(row=0, column=3, padx=1, pady=1, sticky="NSEW")

        btn_7 = self.create_num_btn(7, 1, 0, buttons_frame)
        btn_8 = self.create_num_btn(8, 1, 1, buttons_frame)
        btn_9 = self.create_num_btn(9, 1, 2, buttons_frame)
        btn_sub = self.create_other_btn('-', 1, 3, buttons_frame)

        btn_4 = self.create_num_btn(4, 2, 0, buttons_frame)
        btn_5 = self.create_num_btn(5, 2, 1, buttons_frame)
        btn_6 = self.create_num_btn(6, 2, 2, buttons_frame)
        btn_add = self.create_other_btn('+', 2, 3, buttons_frame)

        btn_1 = self.create_num_btn(1, 3, 0, buttons_frame)
        btn_2 = self.create_num_btn(2, 3, 1, buttons_frame)
        btn_3 = self.create_num_btn(3, 3, 2, buttons_frame)
        btn_dot = Button(buttons_frame, text='.', bd=0, command=self.dot_btn_click)
        btn_dot.grid(row=3, column=3, padx=1, pady=1, sticky="NSEW")

        btn_bracket_open = Button(buttons_frame, text='(', bd=0, command=self.open_bracket_btn_click)
        btn_bracket_open.grid(row=4, column=0, padx=1, pady=1, sticky="NSEW")
        btn_0 = self.create_num_btn(0, 4, 1, buttons_frame)
        btn_bracket_close = Button(buttons_frame, text=')', bd=0, command=self.close_bracket_btn_click)
        btn_bracket_close.grid(row=4, column=2, padx=1, pady=1, sticky="NSEW")
        btn_equals = Button(buttons_frame, text='=', bd=0, bg='lightgrey', command=self.equals_btn_click)
        btn_equals.grid(row=4, column=3, padx=1, pady=1, sticky="NSEW")


if __name__ == '__main__':
    calculator_screen = CalculatorGUI()

    calc = Calculator()
    test = '123+17'  # 140
    print(f'Testing for 140: {calc.calculate(test)}')
    test = '123-17'  # 106
    print(f'Testing for 106: {calc.calculate(test)}')
    test = '123+17+64'  # 204
    print(f'Testing for 204: {calc.calculate(test)}')
    test = '123-17-56'  # 50
    print(f'Testing for 50: {calc.calculate(test)}')
    test = '17+5-4+3-10'  # 11
    print(f'Testing for 11: {calc.calculate(test)}')
    print()
    test = '17+5*4'  # 37
    print(f'Testing for 37: {calc.calculate(test)}')
    test = '17-5*4'  # -3
    print(f'Testing for -3: {calc.calculate(test)}')
    test = '5*4+17'  # 37
    print(f'Testing for 37: {calc.calculate(test)}')
    test = '5*4-17'  # 3
    print(f'Testing for 3: {calc.calculate(test)}')
    test = '17+12/4'  # 20
    print(f'Testing for 20: {calc.calculate(test)}')
    test = '17-12/4'  # 14
    print(f'Testing for 14: {calc.calculate(test)}')
    test = '12/4+17'  # 20
    print(f'Testing for 20: {calc.calculate(test)}')
    test = '12/4-17'  # -14
    print(f'Testing for -14: {calc.calculate(test)}')
    print()
    test = '20+12/4-17'  # 6
    print(f'Testing for 6: {calc.calculate(test)}')
    test = '20-5+3*4-7+15'  # 35
    print(f'Testing for 35: {calc.calculate(test)}')
    print()
    test = '10+(12/4-17)'  # -4
    print(f'Testing for -4: {calc.calculate(test)}')
    test = '(12/4-17)-6'  # -20
    print(f'Testing for -20: {calc.calculate(test)}')
    test = '14+7+(12/4-17)-3+5'  # 9
    print(f'Testing for 9: {calc.calculate(test)}')
    test = '2*(2*4-17)+18'  # 0
    print(f'Testing for 0: {calc.calculate(test)}')
    test = '2*(3*4+10)/4'  # 11
    print(f'Testing for 11: {calc.calculate(test)}')
    test = '2+(3*4+12)/4'  # 8
    print(f'Testing for 8: {calc.calculate(test)}')
    test = '4+3*(3*4-2)/5-5'  # 5
    print(f'Testing for 5: {calc.calculate(test)}')
