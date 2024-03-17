from CreateGUI import *
from tkinter import ttk

from ultralytics import YOLO

from DetectFromPC import hide_detect_from_PC_interface, create_detect_file_interface
from DetectLiveCamera import create_detect_camera_interface, hide_detect_camera_interface
from DetectURL import create_detect_url_interface, hide_detectURL_interface

add_header()
customize()

model = YOLO('yolov8n.pt')


def on_option_selected(event):
    selected_option = option_combobox.get()

    if selected_option == options[0]:
        create_detect_url_interface(application, model)
        hide_detect_from_PC_interface()
        hide_detect_camera_interface()

    elif selected_option == options[1]:
        create_detect_file_interface(application, model)
        hide_detectURL_interface()
        hide_detect_camera_interface()

    elif selected_option == options[2]:
        create_detect_camera_interface(application, model)
        hide_detectURL_interface()
        hide_detect_from_PC_interface()


options = ["Image URL", "Image from PC", "Live Camera"]
option_combobox = ttk.Combobox(application, values=options, state="readonly")
option_combobox.bind("<<ComboboxSelected>>", on_option_selected)
customize_combobox(option_combobox)


application.mainloop()
