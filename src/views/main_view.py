import os
from tkinter import *
from tkinter import messagebox, filedialog
from utils import enum_type

class MainView:
    def __init__(self, controller):
        self.controller = controller

    def display_window(self):
        root = Tk()
        icon = PhotoImage(file="./src/assets/image/eugenio.png")
        root.tk.call('wm', 'iconphoto', root._w, icon)
        root.title("Editor de Teclados para o Eugénio V3")
        root.geometry("500x400")
        root.configure(bg="#F7F9FC")

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

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
        instruction_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.text_widget = Text(root, height=10, width=40, bg="#ECF0F1", fg="#34495E", font=("Arial", 10), bd=0)
        self.text_widget.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        hint_label = Label(
            root,
            text="Digite o nome do teclado:",
            wraplength=450,
            justify="left",
            bg="#F7F9FC",
            fg="#2C3E50",
            font=("Arial", 10),
        )
        hint_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.keyboard_name = Entry(
            root, width=40, bg="#ECF0F1", fg="#34495E", font=("Arial", 10), bd=0, justify="center"
        )
        self.keyboard_name.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        button_frame = Frame(root, bg="#F7F9FC")
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

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

        submit_button = Button(button_frame, text="Criar", command=self._on_submit_click, **button_style)
        submit_button.grid(row=0, column=0, padx=10, sticky="ew")

        edit_button = Button(
            button_frame,
            text="Editar",
            command=self._on_edit_click,
            **{**button_style, "bg": "#2ECC71", "activebackground": "#27AE60"},
        )
        edit_button.grid(row=0, column=1, padx=10, sticky="ew")

        root.mainloop()
        
    def _edit_text(self, content_txt):
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
            self.clearBox()
            self.keyboard_name.insert(0, path)
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
            
    def clearBox(self):
        self.keyboard_name.delete(0, END)
        return
