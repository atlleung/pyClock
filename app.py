## WORSHIP TIMER APP
# Andrew Leung - 2018/03/18
#
# Must be accompanied by timer csv file
#
# Hotkeys:
#  left arrow  - Previous event
#  right arrow - Next Event
#  up arrow    - increase font size
#  down arrow  - decrease font size
#  Escape      - close all windows


import datetime
import time
import pandas as pd
import sys


print("Welcome to the event timer app!\n\n")

print("\nHotkeys for Time window:")
print(  " left arrow  - Previous event \n"
        " right arrow - Next Event \n"
        " up arrow    - increase font size \n"
        " down arrow  - decrease font size \n"
        " Escape Key  - close window/App \n")

#python 2/3 differences

if sys.version_info.major == 2:
    import Tkinter as tk
    name = raw_input("Please enter file name: ")
else:
    import tkinter as tk
    name = input("Please enter file name: ")

# fs = False
df = pd.read_csv(name + ".csv")
font_size = 400

# len(df) = total number of events
counter = 0

## TIMER DISPLAY FUNCTIONS

def StartMove(event):
        root.x = event.x
        root.y = event.y

def StopMove(event):
    root.x = None
    root.y = None

def OnMotion(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry("+%s+%s" % (x, y))


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

# def toggle_fs(event):
#     global root
#     global fs
#     if fs:
#         fs = False
#     else:
#         fs = True
#     root.attributes("-fullscreen", fs)

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


def endApp(event):
    global root
    global control
    root.destroy()
    control.destroy()

def screen_main(event):
    global root
    global width
    global height
    root.geometry('%ix%i' % (width, height))

def screen_half(event):
    global root
    global width
    global height
    root.geometry('%ix%i' % (width/2, height/2))


# CONTROL FUNCTIONS

def control_next():
    global counter
    global df

    print(counter,len(df))
    if counter<(len(df) -1):
        counter += 1

def control_prev():
    global counter
    if counter > 0:
        counter-=1

def c_StartMove(event):
    control.x = event.x
    control.y = event.y

def c_StopMove(event):
    control.x = None
    control.y = None

def c_OnMotion(event):
    deltax = event.x - control.x
    deltay = event.y - control.y
    x = control.winfo_x() + deltax
    y = control.winfo_y() + deltay
    control.geometry("+%s+%s" % (x, y))

y = datetime.datetime.now().year
m = datetime.datetime.now().month
d = datetime.datetime.now().day

# MAIN TIME DISPLAY

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
print(width,height)
# root.attributes("-fullscreen", False)
root.title("countdown timer")
root.geometry('%ix%i' % (width, height))
root.configure(background='black')
root.overrideredirect(True)
#
# c = tk.Canvas(root)
# c.pack(fill="both", expand="YES")

root.bind('<Left>', prev_event)
root.bind('<Right>', next_event)
root.bind('<Prior>', prev_event)
root.bind('<Next>', next_event)
# root.bind('f', toggle_fs)
root.bind('<Up>', up_font)
root.bind('1', screen_main)
root.bind('2', screen_half)
root.bind('<Down>', down_font)
root.bind('<Escape>',endApp)

# dragging motion
root.bind("<ButtonPress-1>", StartMove)
root.bind("<ButtonRelease-1>", StopMove)
root.bind("<B1-Motion>", OnMotion)


label_title = tk.Label(root, fg="white", bg = "black", font ="Helvetica 80")
label_time = tk.Label(root, fg="green", bg = "black", font ="Helvetica " +str(font_size))
label_time.place(relx=.5, rely=.4, anchor="c")
label_title.place(relx=.5, rely=.9, anchor="c")
title_label(label_title)
time_label(label_time)

# button = tk.Button(root, text='Next', width=25, command=next_event(1))
# button.place(relx=.0, rely=.0)

# CONTROL DISPLAY

control = tk.Tk()
control.title("Timer Controller")
control.geometry('%ix%i' % (400, 200))
control.overrideredirect(True)
control_time = tk.Label(control, fg="green",font ="Helvetica 30")
control_label = tk.Label(control, fg="black",font ="Helvetica 30")
control_time.place(relx=.5, rely=.5, anchor="c")
control_label.place(relx=.5, rely=.1, anchor="n")
title_label(control_label)
time_label(control_time)
control_label.pack()
control_prev = tk.Button(control, bg = "gainsboro", text='Previous', width=10, height=3, command = control_prev)
control_prev.place(relx=0.1, rely=.9, anchor="w")
control_next = tk.Button(control, bg = "gainsboro",text='Next', width=10, height=3, command = control_next)
control_next.place(relx=0.9, rely=.9, anchor="e")


# dragging motion
control.bind("<ButtonPress-1>", c_StartMove)
control.bind("<ButtonRelease-1>", c_StopMove)
control.bind("<B1-Motion>", c_OnMotion)
control.bind("<Escape>", endApp)

control.mainloop()
root.mainloop()
