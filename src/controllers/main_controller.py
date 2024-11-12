from models.data_model import DataModel
from views.main_view import MainView
import re


class MainController:
    def __init__(self):
        self.model = DataModel()  
        self.view = MainView(self)  

    def run(self):
        # Possibly fetch data from model (if needed) and display it via the view
        self.view.display_window()

    def on_submit(self, text_widget, keyboard_name):
        # Fetch the text from the Text widget
        user_input = text_widget.get("1.0", "end-1c")  
        keyboard_name = keyboard_name.get("1.0", "end-1c")
        filtred_words = self.filter_words(user_input)  
        print (keyboard_name)
        self.model.search_images(filtred_words, keyboard_name)  # Call the model's search_images method with the filtered words

    def filter_words(self, words):
        # Split the input text into lines to represent rows in the matrix
        lines = words.strip().splitlines()  
        matrix = []

        # Process each line separately
        for line in lines:
            # Find all words within brackets for the current line
            row = re.findall(r"\[(\w+)\]", line)  
            if row:
                matrix.append(row)  # Append the row to the matrix
                print(matrix)
        return matrix

