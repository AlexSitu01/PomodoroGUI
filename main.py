from tkinter import *
import math


reps = 0
timer = None
time_left = 1500
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- Pause Timer ------------------------------- #
#Bug where reps would go to negative numbers if you press pause multiple times i dont want to fix it :)
def pause_timer():
    global reps
    if reps > 0:
        reps -= 1
    window.after_cancel(timer)
    timer_label.config(text="Paused")
    seconds = time_left%60
    if seconds < 10:
        seconds = f"0{seconds}"
    minutes = time_left//60  #rounded down
    if minutes < 10:
        minutes = f"0{minutes}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    checkmark_label.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer(work_sec = WORK_MIN * 60):
    global reps
    reps += 1
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 2 == 1:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Short Break", fg=PINK)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    seconds = count%60
    if seconds < 10:
        seconds = f"0{seconds}"
    minutes = count//60  #rounded down
    if minutes < 10:
        minutes = f"0{minutes}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        checks = ""
        for x in range(reps//2):
            checks += "✔"
        checkmark_label.config(text=checks)
    global time_left
    time_left = count

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx= 100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 114, image=tomato_img)
timer_text = canvas.create_text(103, 130, text="00:00", fill="white",font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)



timer_label = Label(text="Timer",font=(FONT_NAME, 35, "bold"), fg=GREEN, bg= YELLOW)
timer_label.grid(row=0, column= 1)

start_button = Button(text="Start",font=(FONT_NAME, 12, "bold"), command=lambda: start_timer(time_left ))
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset",font=(FONT_NAME, 12, "bold"), command=reset_timer)
reset_button.grid(row=2, column=2)

pause_button = Button(text="Pause",font=(FONT_NAME, 12, "bold"), command=pause_timer)
pause_button.grid(row=3, column=1)

checkmark_label = Label(fg=GREEN, bg=YELLOW)
checkmark_label.grid(row=4, column=1)
window.mainloop()