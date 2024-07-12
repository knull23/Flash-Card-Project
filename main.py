from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
new_card = {}
data_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


def generate_card():
    global new_card, flip_timer
    window.after_cancel(flip_timer)
    new_card = random.choice(data_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=new_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=new_card["English"], fill="white")


def remove_card():
    data_dict.remove(new_card)
    new_data = pandas.DataFrame(data_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    generate_card()


window = Tk()
window.title("Flash Card")
window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)


canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 158, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

right_btn = Button(image=right_img, highlightthickness=0, command=remove_card)
right_btn.grid(row=1, column=1)

wrong_btn = Button(image=wrong_img, highlightthickness=0, command=generate_card)
wrong_btn.grid(row=1, column=0)

generate_card()

window.mainloop()
