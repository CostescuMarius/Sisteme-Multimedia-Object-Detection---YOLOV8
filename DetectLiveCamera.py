import cv2
from PIL import Image, ImageTk
from tkinter import Label, Button, font

image_label = None
error_image_label = None
detect_button = None
info_label = None
stop_detect_button = None

img_x = 60
img_y = 200
detect_button_x = 400
detect_button_y = 730
stop_detect_button_x = 400
stop_detect_button_y = 730
info_label_x = 890
info_label_y = 135

continue_detection = True
cap = None


def create_detect_camera_interface(application, model):
    global image_label, error_image_label, detect_button, stop_detect_button

    if (image_label is None) & (error_image_label is None) & (detect_button is None) & (stop_detect_button is None):
        image_label = Label(application)

        error_image_label = Label(application, text="Error accessing camera", fg="red")

        def detect():
            global info_label, continue_detection, cap

            cap = cv2.VideoCapture(0)

            continue_detection = True
            detect_button.place_forget()
            stop_detect_button.place(x=stop_detect_button_x, y=stop_detect_button_y)

            def start_detection():
                global info_label
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        try:
                            results = model(source=frame, conf=0.4)

                            if info_label is None:
                                info_label = Label(application)

                            info_text = "Results: \n"
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
                            img = img.resize((500, 500))

                            photo = ImageTk.PhotoImage(img)

                            image_label.config(image=photo)
                            image_label.image = photo

                            error_image_label.place_forget()
                            image_label.place(x=img_x, y=img_y)
                        except Exception as e:
                            print("Error during detection:", e)
                    else:
                        print("Error reading frame")
                else:
                    print("Camera not opened")

                if continue_detection:
                    application.after(10, start_detection)

            start_detection()

        detect_button = Button(application, text="Start Detection", command=detect, fg="green", relief="groove",
                               font=("Times New Roman", 11, "bold"))
        detect_button.place(x=detect_button_x, y=detect_button_y)

        def stop_detect():
            global continue_detection
            continue_detection = False

            cap.release()

            detect_button.place(x=detect_button_x, y=detect_button_y)
            stop_detect_button.place_forget()

        stop_detect_button = Button(application, text="Stop Detection", command=stop_detect, fg="red", relief="groove",
                                    font=("Times New Roman", 11, "bold"))

        if cap is not None:
            if not cap.isOpened():
                error_image_label.place(x=img_x, y=img_y)


    else:
        detect_button.place(x=detect_button_x, y=detect_button_y)


def hide_detect_camera_interface():
    global image_label, error_image_label, detect_button, stop_detect_button, info_label, cap

    if (image_label is not None) & (error_image_label is not None):
        image_label.place_forget()
        error_image_label.place_forget()
        if info_label is not None:
            info_label.place_forget()
        if cap is not None:
            cap.release()
        if detect_button is not None:
            detect_button.place_forget()
        if stop_detect_button is not None:
            stop_detect_button.place_forget()