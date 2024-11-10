from tkinter import *

class MainView:
    def __init__(self, controller):
        self.controller = controller

    def display_window(self):
        root = Tk()
        root.title("Image Search and Download")
        root.geometry("500x300")

        # Create a Text widget for input
        text_widget = Text(root, height=10, width=40)
        text_widget.pack(pady=10)
        
        # Create a submit button that will trigger the controller's on_submit method
        submit_button = Button(root, text="Submit", command=lambda: self.controller.on_submit(text_widget))
        submit_button.pack(pady=10)
        
        # Start Tkinter event loop
        root.mainloop()
