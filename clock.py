from tkinter import *
import time

root = Tk()
root.title("Clock")
root.geometry("600x400")


def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    day = time.strftime("%A")
    AP = time.strftime("%p")
    date = time.strftime("%x")
    
    my_clock.config(text= hour + ":" + minute + ":" + " " + AP)
    my_clock.after (1000, clock)
    
    my_clock2.config(text = day + " /" + date + "/")
    
def update():
    my_clock.config(text = "Text")
    
my_clock = Label(root, text = "", font = ("Helvetica", 20), fg = "gray") 
my_clock.pack(pady = 20)

my_clock2 = Label(root, text = " ", font = ("Helvitica", 6))
my_clock2.pack(pady = 10)

clock()
root.mainloop()