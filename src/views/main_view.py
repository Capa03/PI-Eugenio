import os
from tkinter import *
from tkinter import messagebox, filedialog
from utils import enum_type

class MainView:
    def __init__(self, controller):
        self.controller = controller

    def display_window(self):
        root = Tk()
        root.title("Image Search and Download")
        root.geometry("500x400")
        root.configure(bg="#F7F9FC")

        instruction_label = Label(
            root,
            text="Para adicionar pictograma utilize [], para adicionar uma palavra escreva-a.\n"
                 "Escreva as palavras pela ordem que quer que apareçam.",
            wraplength=450,
            justify="left",
            bg="#F7F9FC",
            fg="#2C3E50",
            font=("Arial", 10),
        )
        instruction_label.pack(pady=10)

        self.text_widget = Text(root, height=10, width=40, bg="#ECF0F1", fg="#34495E", font=("Arial", 10), bd=0)
        self.text_widget.pack(pady=10)

        self.keyboard_name = Entry(
            root, width=40, bg="#ECF0F1", fg="#34495E", font=("Arial", 10), bd=0, justify="center"
        )
        self.keyboard_name.insert(0, "Digite o nome do teclado")
        self.keyboard_name.pack(pady=20)

        button_frame = Frame(root, bg="#F7F9FC")
        button_frame.pack(pady=10)

        button_style = {
            "bg": "#3498DB",
            "fg": "#FFFFFF",
            "activebackground": "#2980B9",
            "activeforeground": "#FFFFFF",
            "font": ("Arial", 10, "bold"),
            "bd": 0,
            "width": 12,
            "height": 2,
        }

        submit_button = Button(button_frame, text="Submit", command=self._on_submit_click, **button_style)
        submit_button.pack(side=LEFT, padx=10)

        edit_button = Button(
            button_frame,
            text="Edit",
            command=self._on_edit_click,
            **{**button_style, "bg": "#2ECC71", "activebackground": "#27AE60"},
        )
        edit_button.pack(side=LEFT, padx=10)

        root.mainloop()
        
    def _edit_text(self, content_txt):
        #print(txt)
        self.text_widget.delete(1.0, "end-1c")
        self.text_widget.insert("end-1c", content_txt)



    def _on_edit_click(self):
        """
        Handles the Edit button click event, opens file picker in a specific folder.
        """
        # Define the default folder path
        appdata_dir = os.getenv('APPDATA')  # Path to %APPDATA%
        target_folder = os.path.join(appdata_dir, "LabSI2-INESC-ID", "Eugénio 3.0")

        # Open file dialog and restrict to `.tec` files
        file_path = filedialog.askopenfilename(
            initialdir=target_folder,
            title="Select a .tec file to edit",
            filetypes=(("TEC Files", "*.tec"), ("All Files", "*.*"))
        )
        
        if file_path:  # If a file is selected
            path = os.path.basename(file_path).replace(".tec", "")
            print("LOCAL: ", path)
            self.controller.on_edit(path)

    def _on_submit_click(self):
        user_input = self.text_widget.get("1.0", "end-1c").strip()
        keyboard_name = self.keyboard_name.get().strip()
        self.controller.on_submit(user_input, keyboard_name)

    def show_error(self, type, message):
        if type == enum_type.Message.ERROR:
            messagebox.showerror("Error", message)
        elif type == enum_type.Message.SUCCESS:
            messagebox.showinfo("Success", message)
