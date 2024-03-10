import tkinter as tk
import ttkbootstrap as ttk
import ctypes as ct
import qrcode
import tempfile
import os
import win32clipboard as w32cl
from io import BytesIO
from PIL import Image


def delete_temp_file(temp_file):
    try:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except Exception as e:
        print(e)


def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img_file:
        img.save(temp_img_file.name)
        temp_img_file_path = temp_img_file.name
        file_to_remove = temp_img_file_path

    return temp_img_file_path, file_to_remove


class App(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Config
        self.update()
        self.geometry("800x600")
        self.minsize(800, 600)
        self.title("QR Code Maker")
        self.qr, self.old_temp_file = generate_qr("https://github.com/Germi32")
        self.dark_title_bar()
        # Frames
        self.header = ttk.Frame(self)

        self.url_label = ttk.Label(self.header, text="URL:")
        self.url_entry = ttk.Entry(self.header)
        self.btn_generate = ttk.Button(self.header, text="Generate", command=self.insert_qr,
                                       bootstyle=(ttk.SUCCESS, ttk.OUTLINE))

        self.image = ttk.PhotoImage(file=self.qr)
        self.img = ttk.Label(self, image=self.image)

        self.btn_copy = ttk.Button(self, text="Copy to clipboard", command=self.copy_to_clipboard,
                                   bootstyle=ttk.LIGHT)
        # Grid config
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)

        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=90)
        self.header.columnconfigure(2, weight=1)
        # Layout
        self.header.grid(row=0, column=0, sticky="new", padx=10, pady=10)

        self.url_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.url_entry.grid(row=0, column=1, sticky=tk.NSEW)
        self.btn_generate.grid(row=0, column=2, sticky="nse")

        self.img.grid(row=1, column=0)

        self.btn_copy.grid(row=2, column=0, sticky=tk.N, pady=(0, 50))

    def insert_qr(self):
        url = self.url_entry.get()
        to_delete = self.old_temp_file
        self.qr, self.old_temp_file = generate_qr(url)
        self.image.configure(file=self.qr)
        self.img.configure(image=self.image)
        delete_temp_file(to_delete)

    def copy_to_clipboard(self):
        image = Image.open(self.qr)

        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()

        w32cl.OpenClipboard()
        w32cl.EmptyClipboard()
        w32cl.SetClipboardData(w32cl.CF_DIB, data)
        w32cl.CloseClipboard()

    def dark_title_bar(self):
        DARK_MODE = 20  # Rendering policy attribute
        hwnd = ct.windll.user32.GetParent(self.winfo_id())
        value = ct.c_int(2)
        ct.windll.dwmapi.DwmSetWindowAttribute(hwnd, DARK_MODE, ct.byref(value), ct.sizeof(value))


icon, _ = generate_qr("https://www.google.com/")

app = App(themename="vapor", iconphoto=icon)

app.mainloop()

delete_temp_file(app.old_temp_file)
delete_temp_file(icon)
