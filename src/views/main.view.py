import tkinter as tk

class MainView:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My Desktop App")

    def set_controller(self, controller):
        self.controller = controller

    def run(self):
        self.window.mainloop()
