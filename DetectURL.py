import tkinter.ttk

import cv2
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import Label, StringVar, Entry, font, Button

image_label = None
error_image_label = None
image = None
find_button = None
detect_button = None
url_entry = None
info_label = None

img_x = 60
img_y = 200
url_x = 60
url_y = 140
find_button_x = 690
find_button_y = 135
detect_button_x = 400
detect_button_y = 730
info_label_x = 890
info_label_y = 135

new_width = None
new_height = None


def create_detect_url_interface(application, model):
    global image_label, error_image_label, find_button, detect_button, url_entry

    if (image_label is None) & (error_image_label is None) & (find_button is None) & (
            detect_button is None) & (url_entry is None):
        image_label = Label(application)

        error_image_label = Label(application, text="The photo was not found", fg="red")

        def find():
            global image, new_width, new_height
            try:
                url = url_entry_var.get()
                response = requests.get(url)

                image = Image.open(BytesIO(response.content))

                aspect_ratio = image.width / image.height
                max_width = 780
                max_height = 500

                new_width = min(image.width, max_width)
                new_height = min(image.height, max_height)

                if (new_width == image.width) and (new_height != image.height):
                    new_width = int(image.width * aspect_ratio)
                elif (new_width != image.width) and (new_height == image.height):
                    new_height = int(image.height * aspect_ratio)
                elif (new_width != image.width) and (new_height != image.height):
                    if int(image.height * aspect_ratio) <= max_height:
                        new_height = int(image.height * aspect_ratio)
                    elif int(image.width * aspect_ratio) <= max_width:
                        new_width = int(image.width * aspect_ratio)

                image = image.resize((new_width, new_height))

                photo = ImageTk.PhotoImage(image)

                image_label.config(image=photo)
                image_label.image = photo

                error_image_label.place_forget()
                image_label.place(x=img_x, y=img_y)

            except Exception as e:
                image_label.place_forget()
                error_image_label.place(x=img_x, y=img_y)

        url_entry_var = StringVar()
        url_entry = Entry(application, textvariable=url_entry_var, width=100)
        url_entry.place(x=url_x, y=url_y)

        find_button = Button(application, text="Find", command=find, foreground="blue", relief="groove", font=("Times New Roman", 11, "bold"))
        find_button.place(x=find_button_x, y=find_button_y)

        def detect():
            global image, new_width, new_height, info_label
            if image is not None:
                try:
                    if info_label is None:
                        info_label = Label(application)

                    info_text = "Results: \n"
                    results = model(source=image, conf=0.4)

                    verbose_results = results[0].verbose()
                    info_tokens = [token.strip() for token in verbose_results.split(',')]

                    for token in info_tokens:
                        info_text += f"    {token}\n"

                    info_label.config(text=info_text, anchor="w", justify="left",
                                      font=font.Font(family="Times New Roman", size=12, weight="bold"))
                    info_label.place(x=info_label_x, y=info_label_y)

                    img_np = results[0].plot()

                    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

                    img = Image.fromarray(img_np)
                    img = img.resize((new_width, new_height))

                    photo = ImageTk.PhotoImage(img)

                    image_label.config(image=photo)
                    image_label.image = photo

                    error_image_label.place_forget()
                except Exception as e:
                    print("Error during detection:", e)
            else:
                print("No image to detect")

        detect_button = Button(application, text="Detect", command=detect, fg="green", relief="groove", font=("Times New Roman", 11, "bold"))
        detect_button.place(x=detect_button_x, y=detect_button_y)

    else:
        url_entry.place(x=url_x, y=url_y)
        find_button.place(x=find_button_x, y=find_button_y)
        detect_button.place(x=detect_button_x, y=detect_button_y)


def hide_detectURL_interface():
    global image_label, error_image_label, find_button, detect_button, url_entry, info_label

    if (image_label is not None) & (error_image_label is not None) & (find_button is not None) & (
            detect_button is not None) & (url_entry is not None):
        image_label.place_forget()
        error_image_label.place_forget()
        find_button.place_forget()
        detect_button.place_forget()
        url_entry.delete(0, 'end')
        url_entry.place_forget()
        if info_label is not None:
            info_label.place_forget()
