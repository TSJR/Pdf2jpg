import pdf2image
import os
import stitching
from PIL import Image
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font
from PIL import ImageTk, Image
import time

path = os.path.dirname(os.path.abspath(__file__))
pages_dir = os.path.join(path, "pages")


def get_end(url):
    return url[url.rfind("/") + 1 :]


while len(path) > 0 and not get_end(path) in [
    "Documents",
    "Downloads",
    "Desktop",
    "Applications",
]:
    path = path[0 : path.rfind("/")]


if not os.path.exists(pages_dir):
    os.mkdir(pages_dir)

img_names = []

filename = ""

pil_img = None

pdf = ""

window = tk.Tk()
window.title("PDF to JPG")
window.geometry("800x400")
window.configure(bg="#d1d1d1")

frame = tk.Frame(master=window, bg="#d1d1d1")
frame.pack(side=tk.BOTTOM, pady=50)
frame2 = tk.Frame(master=window, bg="#d1d1d1")
frame2.pack(side=tk.TOP, pady=50)

img_label = Label(
    master=frame2,
    text=f"Selected pdf: None",
    font=("Helvetica", 32),
    background="#d1d1d1",
)
img_label.grid(row=0, column=1, padx=5, pady=5)

status_label = Label(
    master=frame2,
    text=f"",
    font=("Helvetica", 32),
    background="#d1d1d1",
    foreground="#009c00",
)
status_label.grid(row=1, column=1, padx=5, pady=5)
count = 0


def send_img():
    global pdf, status_label, img_names, img_label

    status_label.config(foreground="#009c00")
    success = True
    img_names = []
    if not pdf:
        success = False
    try:
        print("sending")
        status_label.config(text=path)

        pages = pdf2image.convert_from_path(
            os.path.join(path, pdf), poppler_path=r"/opt/homebrew/bin/"
        )

        for i in range(len(pages)):
            pages[i].save(os.path.join(pages_dir, f"page{i}.jpg"), "JPEG")
            img_names.append(os.path.join(pages_dir, f"page{i}.jpg"))

        imgs = [Image.open(img_name) for img_name in img_names]

        width = max(img.width for img in imgs)
        height = sum(img.height for img in imgs)

        output = Image.new("RGB", (width, height))
        cur_height = 0
        for img in imgs:
            output.paste(im=img, box=(0, cur_height))
            cur_height += img.height
        output.save(os.path.join(path, f"{pdf[:-4]}.jpg"))
        status_label.config(text="Done")
        
    except Exception as error:
        success = False
        status_label.config(text=error)
    if not success:
        status_label.config(text="Please try again. Error: " + error)
        status_label.config(foreground="#c90202")
        pdf = None
        img_label.config(text=f"Selected pdf: None")


def get_img():
    global pdf, img_label, status_label

    filename = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf = filename
    while "/" in filename:
        filename = filename[filename.index("/") + 1 :]

    img_label.config(text=f"Selected pdf: {filename}")
    status_label.config(text="")


file_upload = tk.Button(
    master=frame,
    text="Upload",
    width=25,
    height=2,
    bg="white",
    fg="black",
    command=lambda: get_img(),
)
send = tk.Button(
    master=frame,
    text="Convert",
    width=25,
    height=2,
    bg="white",
    fg="black",
    command=lambda: send_img(),
)

file_upload["font"] = font.Font(family="Helvetica", size=24)
send["font"] = font.Font(family="Helvetica", size=24)

file_upload.grid(row=1, column=0, padx=5, pady=5)
send.grid(row=1, column=1, padx=5, pady=5)

window.mainloop()
