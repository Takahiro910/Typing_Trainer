from tkinter import *
import random
import math
import os


BG_COLOR = "#B1DDC6"
MAIN_COLOR = "#74B49B"
FG_COLOR = "#FFFFFF"
ACCENT_COLOR = "#FFFFFF"
FONT_FAMILY = "Arial"
TIME = 60 #sec
INPUT = ""
timer = ""
counter = 0


def start(event):
    global running
    if not running:
        if not event.keycode in [16, 17, 18]:
            running = True
            count_down(TIME)
            reset_button.config(state="normal")
            log_button.config(state="disabled")

    if not canvas.itemcget(text, 'text').startswith(input_entry.get()):
        input_entry.config(fg="red")
    else:
        input_entry.config(fg="black")

    if input_entry.get() == canvas.itemcget(text, 'text'):
        global INPUT
        INPUT += (input_entry.get() + " ")
        input_entry.delete(0, END)
        canvas.itemconfig(text, text=random.choice(texts))


def count_down(count):
    count_min = str(math.floor(count / 60))
    count_sec = str(count % 60)
    canvas.itemconfig(timer_text, text=f"{count_min.zfill(2)}:{count_sec.zfill(2)}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down,  count - 1)
    else:
        global running
        running = False
        global INPUT
        last_input = input_entry.get()
        last_text = canvas.itemcget(text, 'text')
        result = ""
        for i in range(0, len(last_input)):
            if last_input[:i] in last_text:
                result =last_input[:i]
        INPUT += result
        post_record()


def reset():
    global running
    running = False

    global timer
    window.after_cancel(timer)

    global INPUT
    INPUT = ""

    input_entry.config(state='normal')
    input_entry.delete(0, END)

    canvas.itemconfig(card, image=card_image)
    canvas.itemconfig(timer_text, state="normal", text=test_time)
    canvas.itemconfig(text, text=random.choice(texts), fill="#000000")
    input_entry.place(x=400, y=300, anchor="center")
    input_entry.focus_set()
    log_button.config(state="normal")


def post_record():
    cpm = len(INPUT) / TIME * 60
    wpm = len(INPUT.split()) / TIME * 60
    output = [f"{cpm:.1f}", f"{wpm:.1f}"]
    bs_file = "best_score.txt"
    if not os.path.exists(bs_file):
        with open(bs_file, "w") as file:
            file.write("\n".join(output))
        best = output
    else:
        with open(bs_file, "r") as file:
            best = [s.strip() for s in file.readlines()]
        if cpm > float(best[0]):
            with open(bs_file, "w") as file:
                file.write("\n".join(output))

    canvas.itemconfig(card, image=card_back_image)
    canvas.itemconfig(timer_text, state="hidden")
    canvas.itemconfig(text, text=f"Result\n{cpm:.1f} cpm / {wpm:.1f} wpm\n\nBest\n{best[0]} cpm / {best[1]} wpm", justify="center", fill=FG_COLOR)
    input_entry.place_forget()


def get_record():
    best = ["0.0", "0.0"]
    bs_file = "best_score.txt"
    if os.path.exists(bs_file):
        with open(bs_file, "r") as file:
            best = [s.strip() for s in file.readlines()]

    canvas.itemconfig(card, image=card_back_image)
    canvas.itemconfig(timer_text, state="hidden")
    canvas.itemconfig(text, text=f"Best\n{best[0]} cpm / {best[1]} wpm", justify="center", fill=FG_COLOR)
    input_entry.place_forget()
    log_button.config(text="Start", command=return_start)


def return_start():
    canvas.itemconfig(card, image=card_image)
    canvas.itemconfig(timer_text, state="normal")
    canvas.itemconfig(text, text=random.choice(texts), fill=MAIN_COLOR)
    input_entry.place(x=400, y=300, anchor="c")
    input_entry.delete(0, END)
    input_entry.focus_set()
    log_button.config(text="Record", command=get_record)


# --- UI SETING --- #
window = Tk()
window.title('Typing Test')
window.geometry("+200-50")
window.config(bg=BG_COLOR, pady=40, padx=40)

title_label = Label(text="Typing Trainer", font=("Courier", 35, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
title_label.grid(row=0, columnspan=2, pady=10)

canvas = Canvas(height=526, width=800, bg=BG_COLOR, highlightthickness=0)
card_image = PhotoImage(file="images/card.png")
card_back_image = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_image)
texts = open('type_words.txt', 'r', encoding="utf-8").read().split('\n')
text = canvas.create_text(400, 200, text=random.choice(texts), font=("Arial", 30, "bold"), width=700)
input_entry = Entry(canvas, width=35, font=(FONT_FAMILY, 24), bg="#FFFFFF", justify="center")
input_entry.place(x=400, y=300, anchor="c")
input_entry.focus_set()
input_entry.bind("<KeyRelease>", start)

test_time = f"{str(TIME//60).zfill(2)}:{str(TIME % 60).zfill(2)}"
timer_text = canvas.create_text(400, 100, text=test_time, fill=MAIN_COLOR, font=(FONT_FAMILY, 35, "bold"))
canvas.grid(row=1, columnspan=2)

reset_button = Button(text="Reset", command=reset, font=(FONT_FAMILY, 24), bg=MAIN_COLOR, fg=FG_COLOR, borderwidth=0, activebackground="#5C8D89", activeforeground=FG_COLOR, width=12, state="disable")
reset_button.grid(row=2, column=1, padx=5)

log_button = Button(text="Record", command=get_record, font=(FONT_FAMILY, 24), bg=MAIN_COLOR, fg=FG_COLOR, borderwidth=0, activebackground="#5C8D89", activeforeground=FG_COLOR, width=12)
log_button.grid(row=2, column=0, padx=5)

# self.main_frame.pack(expand=True)

counter = 0
running = False

window.mainloop()