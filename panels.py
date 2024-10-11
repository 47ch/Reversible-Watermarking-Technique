import customtkinter as ctk

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.pack(fill = 'x', pady = 4, ipady = 4)

class WatermarkingMethod(Panel):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)

        my_font = ctk.CTkFont(family="Helvetica ", weight = "bold")

        ctk.CTkLabel(self, text=text, font=my_font).grid(column=0, row=0, stick = 'w', padx = 5)
        ctk.CTkOptionMenu(self, values=["Method 1", "Method 2"], font=my_font).grid(column = 1, row = 0, stick = 'e', padx = 5)

class InputBox(Panel):
    def __init__(self, parent, text = 'Enter the text to watermark:'):
        super().__init__(parent)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)

        my_font = ctk.CTkFont(family="Helvetica ", weight = "bold")
        ctk.CTkLabel(self, text=text, font=my_font).grid(column=0, row=0, stick = 'w', padx = 3)

        self.textbox = ctk.CTkTextbox(master = self, height = 10)
        self.textbox.grid(column = 1, row=0, sticky="e")
        self.textbox.insert("0.0", "Enter")