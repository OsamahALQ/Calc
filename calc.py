import tkinter as tk
from tkinter import messagebox
import math

calculation_history = []

def create_complete_calculator():
	# Create the main window for the calculator
	root = tk.Tk()
	root.title("Complete Fancy Calculator")
	root.geometry("450x600")

	# Variable to keep track of input/output
	global expression, result_expression
	expression = tk.StringVar()
	result_expression = tk.StringVar()

	global display
	display = tk.Text(root, height=2, width=22, font=("Consolas", 20, "bold"), bd=10)
	display.grid(row=0, column=0, columnspan=5)



	num_button_color = "#222831"
	op_button_color = "#393E46"
	func_button_color = "#00ADB5"

	root.config(bg="#222831")

	buttons = [
		('7', 2, 0, num_button_color),
		('8', 2, 1, num_button_color),
		('9', 2, 2, num_button_color),
		('/', 2, 3, op_button_color),
		('4', 3, 0, num_button_color),
		('5', 3, 1, num_button_color),
		('6', 3, 2, num_button_color),
		('*', 3, 3, op_button_color),
		('1', 4, 0, num_button_color),
		('2', 4, 1, num_button_color),
		('3', 4, 2, num_button_color),
		('-', 4, 3, op_button_color),
		('C', 2, 4, func_button_color),
		('0', 5, 1, num_button_color),
		('=', 5, 2, func_button_color),
		('+', 5, 3, op_button_color),
		('sin', 6, 0, func_button_color),
		('cos', 6, 1, func_button_color),
		('tan', 6, 2, func_button_color),
		('√', 6, 3, func_button_color),
		('x²', 6, 4, func_button_color),
		('←', 3, 4, func_button_color),
  		('.', 5, 0, num_button_color),
		('exp', 7, 2, func_button_color),
		('1/x', 7, 3, func_button_color),
		(')', 5, 4, op_button_color),
		('(', 4, 4, op_button_color),
		('π', 7, 4, func_button_color),
		('log', 7, 0, func_button_color),
		('ln', 7, 1, func_button_color),
		('History', 8, 4, func_button_color)
	]

	for (text, row, col, bg_color) in buttons:	 
		button = tk.Button(root, text=text, font=("Arial", 12, "bold"), bg=bg_color, fg="white",
						command=lambda value=text: on_button_press(value))
		button.grid(row=row, column=col, sticky="nsew", ipadx=20, ipady=20)

	global constants_menu
	constants_menu = create_constants_menu(root)
	root.bind("<Button-3>", on_right_click)

	adv_display_button = tk.Button(root, text="Adv Display", bg=func_button_color, fg="white", command=advanced_display_mode)
	adv_display_button.grid(row=8, column=0, sticky="nsew", ipadx=20, ipady=20, columnspan=4)

	for i in range(5):
		root.grid_columnconfigure(i, weight=1)
	for i in range(9):
		root.grid_rowconfigure(i, weight=1)

	return root

def show_history():
	history_window = tk.Toplevel()
	history_window.title("Calculation History")
	history_text = tk.Text(history_window, height=10, width=50)
	history_text.pack()
	for calc in calculation_history:
		history_text.insert(tk.END, calc + "\n")

def on_button_press(value):
    global display, calculation_history
    try:
        display.config(state=tk.NORMAL)  # Enable text widget changes
        current_expression = display.get("1.0", "end-1c").rstrip()  # Get the current content

        if value == "C":
            display.delete('1.0', tk.END)  # Clear the display
        elif value == "←":
            if len(current_expression) > 1:
                new_expression = current_expression[:-1]
                display.delete('1.0', tk.END)
                display.insert(tk.END, new_expression)
            else:
                display.delete('1.0', tk.END)
        elif value == "=":
            # Do not show the "=" sign in the display
            result = str(evaluate_expression(current_expression))
            # Align the result to the bottom right
            result_line = result.rjust(22)  # Adjust 22 according to the width of your Text widget
            display.insert(tk.END, "\n" + result_line)
            calculation_history.append(f"{current_expression} = {result}")
            # Move the cursor to the end to scroll down to the result
            display.see(tk.END)
            # Modify this part of your on_button_press function
        elif value == 'sin':
            display.insert(tk.END, 'sin(')
        elif value == 'cos':
            display.insert(tk.END, 'cos(')
        elif value == 'tan':
            display.insert(tk.END, 'tan(')
        elif value == 'ln':
            # For trigonometric functions and natural log, insert the value followed by an open parenthesis
            display.insert(tk.END, value + "ln(")
        elif value in ('√', 'x²', 'log', 'exp', '1/x', 'π'):
            current_expression = insert_advanced_operation(display.get("1.0", tk.END).strip(), value)
            display.delete('1.0', tk.END)
            display.insert(tk.END, current_expression)
        elif value == 'History':
            show_history()
        else:
            # If the current expression is just "0", replace it with the new value
            if current_expression == "0":
                display.delete('1.0', tk.END)
            # Insert the value to the display
            display.insert(tk.END, value)

        display.config(state=tk.DISABLED)  # Disable text widget changes after update
    except Exception as e:
        display.delete('1.0', tk.END)  # Clear the display
        display.insert(tk.END, "Error")  # Show the error message
        display.config(state=tk.DISABLED)

def evaluate_expression(expression):
    try:
        # Replace math functions and constants with their Python equivalents
        expression = expression.replace("π", "math.pi")
        expression = expression.replace("sin(", "math.sin(math.radians(")
        expression = expression.replace("cos(", "math.cos(math.radians(")
        expression = expression.replace("tan(", "math.tan(math.radians(")
        expression = expression.replace("ln(", "math.log(")
        expression = expression.replace("log(", "math.log10(")
        expression = expression.replace("exp(", "math.exp(")
        expression = expression.replace("√(", "math.sqrt(")
        expression = expression.replace("x²", "**2")
        expression = expression.replace("1/x", "1/")

        # Evaluate safely
        return eval(expression, {"__builtins__": None, "math": math})
    except Exception as e:
        return "Error"


def insert_advanced_operation(expression, operation):
    # Insert the advanced operation into the expression with proper syntax
    if operation == 'π':
        return expression + "π"
    elif operation == 'sin':
        return expression + "sin("
    elif operation == 'cos':
        return expression + "cos("
    elif operation == 'tan':
        return expression + "tan("
    elif operation == '√':
        return expression + "√("
    elif operation == 'x²':
        return expression + "**2"
    elif operation == 'ln':
        # Since "log" in Python is the natural log, use "log" for ln
        return expression + "ln("
    elif operation == 'log':
        return expression + "log10("
    elif operation == 'exp':
        return expression + "exp("
    elif operation == '1/x':
        return expression + "1/("
    return expression

def advanced_display_mode():
	messagebox.showinfo("Info", "Advanced display mode is not yet implemented.")

def insert_constant(constant_value):
	current_expression = expression.get()
	expression.set(current_expression + str(constant_value))

def create_constants_menu(root):
	menu = tk.Menu(root, tearoff=0)
	constants = {
		"π": math.pi,
		"e": math.e,
		"φ (Golden Ratio)": (1 + math.sqrt(5)) / 2,
		"h (Planck Constant)": 6.62607015e-34
	}
	for const, value in constants.items():
		menu.add_command(label=f"{const}", command=lambda v=value: insert_constant(v))
	return menu

def on_right_click(event):
	try:
		constants_menu.tk_popup(event.x_root, event.y_root)
	finally:
		constants_menu.grab_release()

def test_complete_calculator():
	app = create_complete_calculator()
	app.mainloop()

# Uncomment the line below to run the complete calculator for testing
test_complete_calculator()

