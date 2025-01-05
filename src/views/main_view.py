from tkinter import *
from tkinter import messagebox
from utils import enum_type

class MainView:
    def __init__(self, controller):
        self.controller = controller

    def display_window(self):
        root = Tk()
        root.title("Image Search and Download")
        root.geometry("500x300")

        # Create a Text widget for input
        self.text_widget = Text(root, height=10, width=40)
        self.text_widget.pack(pady=10)

        # Create a Text widget for creating the name of the keyboard
        self.keyboard_name = Entry(root, width=40)
        self.keyboard_name.pack(pady=20)

        # Create a submit button that will trigger the controller's on_submit method
        submit_button = Button(root, text="Submit", command=self._on_submit_click)
        submit_button.pack(pady=10)

        
        edit_button = Button(root, text="Edit", command=self._on_edit_click)
        edit_button.pack(pady=5)

        # Start Tkinter event loop
        root.mainloop()

    def _edit_text(self, txt):
        #print(txt)
        self.text_widget.delete(1.0, "end-1c")
        self.text_widget.insert("end-1c", txt)

    def _on_edit_click(self):
        """
        Lida com o evento de clique no botão de editar.
        """
        #user_input = self.text_widget.get("1.0", "end-1c").strip()
        #self._edit_text()
        keyboard_name = self.keyboard_name.get().strip()
        self.controller.on_edit(keyboard_name)

    def _on_submit_click(self):
        """
        Lida com o evento de clique no botão de envio.
        """
        user_input = self.text_widget.get("1.0", "end-1c").strip()
        keyboard_name = self.keyboard_name.get().strip()
        self.controller.on_submit(user_input, keyboard_name)

    def show_error(self, type, message):
        """
        Exibe uma modal de erro ao usuário.
        """
        if(type == enum_type.Message.ERROR):
            messagebox.showerror("Error", message)
        if(type == enum_type.Message.SUCCESS):
            messagebox.showinfo("Success", message)