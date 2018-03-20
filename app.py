## WORSHIP TIMER APP
# Andrew Leung - 2018/03/18
#
# Must be accompanied by timer csv file
#
# Hotkeys:
#  f           - toggle full screen
#  left arrow  - Previous event
#  right arrow - Next Event
#  up arrow    - increase font size
#  down arrow  - decrease font size

import Tkinter as tk
import datetime
import time
import pandas as pd

print("\nHotkeys:")
print(  " f           - toggle full screen \n"
        " left arrow  - Previous event \n"
        " right arrow - Next Event \n"
        " up arrow    - increase font size \n"
        " down arrow  - decrease font size \n")

name = raw_input("Please enter file name: ")
fs = False
df = pd.read_csv(name + ".csv")
font_size = 600

# len(df) = total number of events
counter = 0

def title_label(label):
  def count():
    global counter
    label.config(text=df["event"][counter])
    label.after(100, count)
  count()

def time_label(label):
  def count():
    global counter
    t_event = datetime.datetime(y,m,d,df["hour"][counter], df["minute"][counter])
    delta = t_event - datetime.datetime.now()

    if int(delta.days) <0:
        label.config(fg = "red")
        dm, ds= divmod(abs(int(delta.seconds-86400)), 60)
        if ds <10:
            ds = str(0)+str(ds)
        label.config(text=str(dm) + ":" + str(ds))
    else:
        label.config(fg = "green")
        dm, ds= divmod(abs(int(delta.seconds)), 60)
        if dm > 2:
            label.config(text=str(dm))
        elif ds < 10:
            ds = str(0)+str(ds)
            label.config(text=str(dm) + ":" + str(ds))
        else:
            label.config(text=str(dm) + ":" + str(ds))

    label.after(100, count)
  count()

def next_event(event):
    global counter
    global df
    global root

    print(counter,len(df))
    if counter<(len(df) -1):
        counter += 1

def prev_event(event):
    global counter
    if counter > 0:
        counter-=1

def toggle_fs(event):
    global root
    global fs
    if fs:
        fs = False
    else:
        fs = True
    root.attributes("-fullscreen", fs)

def up_font(event):
    global font_size
    global tabel_time
    font_size += 10
    label_time.configure(font = "Helvetica " +str(font_size))


def down_font(event):
    global font_size
    global tabel_time
    font_size -= 10
    label_time.configure(font = "Helvetica " +str(font_size))

y = datetime.datetime.now().year
m = datetime.datetime.now().month
d = datetime.datetime.now().day

root = tk.Tk()
root.attributes("-fullscreen", False)
root.title("countdown timer")
root.geometry("1600x1000")
root.configure(background='black')
#
# c = tk.Canvas(root)
# c.pack(fill="both", expand="YES")

root.bind('<Left>', prev_event)
root.bind('<Right>', next_event)
root.bind('<Prior>', prev_event)
root.bind('<Next>', next_event)
root.bind('f', toggle_fs)
root.bind('<Up>', up_font)
root.bind('<Down>', down_font)
root.bind('<Escape>',toggle_fs)

label_title = tk.Label(root, fg="white", bg = "black", font ="Helvetica 140")
label_time = tk.Label(root, fg="green", bg = "black", font ="Helvetica " +str(font_size))
label_time.place(relx=.5, rely=.4, anchor="c")
label_title.place(relx=.5, rely=.9, anchor="c")
title_label(label_title)
time_label(label_time)

# button = tk.Button(root, text='Next', width=25, command=next_event(1))
# button.place(relx=.0, rely=.0)


root.mainloop()
