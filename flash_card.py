# IMPORT
from tkinter import *
import pandas
import random

# CONSTANT
CARD_FRONT_PATH = r"E:\Learning\Python\Python_Projects\Flash_Card\images\card_front.png"
CARD_BACK_PATH = r"E:\Learning\Python\Python_Projects\Flash_Card\images\card_back.png"

RIGHT_PATH = r"E:\Learning\Python\Python_Projects\Flash_Card\images\right.png"
WRONG_PATH = r"E:\Learning\Python\Python_Projects\Flash_Card\images\wrong.png"

DATA_PATH = r"E:\Learning\Python\Python_Projects\Flash_Card\data\french_words.csv"
DATA_TO_LEARN_PATH = r"E:\Learning\Python\Python_Projects\Flash_Card\data\words_to_learn.csv"

GREEN = "#b1dcc7"

current_card = {}
data_dict = []

# ----------------------------- READING CSV --------------------------------- #
try:
	data_dataframe = pandas.read_csv(DATA_TO_LEARN_PATH)

except FileNotFoundError:
	original_data_dataframe = pandas.read_csv(DATA_PATH)
	data_dict = original_data_dataframe.to_dict(orient="records")

else:
	data_dict = data_dataframe.to_dict(orient="records")

# ----------------------------- FUNCTIONS --------------------------------- #
def next_card():
	global current_card, flip_timer
	window.after_cancel(flip_timer)
	current_card = random.choice(data_dict)
	canvas.itemconfig(canvas_title, text="French", fill="black")
	canvas.itemconfig(canvas_word, text=current_card["French"], fill="black")
	canvas.itemconfig(canvas_background, image=first_image)
	flip_timer = window.after(3000, func=flip_card)

def flip_card():
	canvas.itemconfig(canvas_title, text="English", fill="white")
	canvas.itemconfig(canvas_word, text=current_card["English"], fill="white")
	canvas.itemconfig(canvas_background, image=second_image)

def is_known():
	data_dict.remove(current_card)
	print(len(data_dict))
	data_dataframe2 = pandas.DataFrame(data_dict)
	# index=False is to prevent duplicate indexes
	data_dataframe2.to_csv(DATA_TO_LEARN_PATH, index=False)

	next_card()

# ----------------------------- UI SETUP ---------------------------------- #
# Tk
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=GREEN)

flip_timer = window.after(3000, func=flip_card)

# Canvas
# Canvas Card
canvas = Canvas(width=800, height=526, bg=GREEN, highlightthickness=0)

first_image = PhotoImage(file=CARD_FRONT_PATH)
second_image = PhotoImage(file=CARD_BACK_PATH)

canvas_background = canvas.create_image(400, 263, image=first_image)
canvas.grid(row=0, column=0, columnspan=2)

# Canvas Title
canvas_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"), text="")
# Canvas Word
canvas_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"), text="")

# Button
# Button Right
image_right = PhotoImage(file=RIGHT_PATH)
button_right = Button(image=image_right, highlightthickness=0, borderwidth=0, bg=GREEN, command=is_known)
button_right.grid(row=1, column=1)

# Button Wrong
image_wrong = PhotoImage(file=WRONG_PATH)
button_wrong = Button(image=image_wrong, highlightthickness=0, borderwidth=0, bg=GREEN, command=next_card)
button_wrong.grid(row=1, column=0)

# Calling function
next_card()

# Last
window.mainloop()