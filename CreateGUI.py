from tkinter import *

WIDTH = 1300
HEIGHT = 790

application = Tk()

def customize():
    application.title("Object Detection")
    application.minsize(width=WIDTH, height=HEIGHT)
    application.maxsize(width=WIDTH, height=HEIGHT)

    canvas = Canvas(application, width=WIDTH, height=HEIGHT)
    canvas.pack()
    x = WIDTH * 2 / 3
    canvas.create_line(x, 0, x, HEIGHT, fill="black")


def add_header():
    header = Frame(application, width=WIDTH, bg="#6495ED")
    header.pack(side="top", fill="x")

    header_label = Label(header, height=2, text="Object Detection", fg="white", bg="#6495ED",
                         font=("Times New Roman", 16, "bold"))
    header_label.pack(side="left", padx="10")


def customize_combobox(option_combobox):
    header_option = Label(text="Choose the option:", fg="black", font=("Times New Roman", 13))
    header_option.place(x=60, y=100)
    option_combobox.place(x=200, y=100)

