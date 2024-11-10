from models.data_model import DataModel
from views.main_view import MainView

import re
import os

class MainController:
    def __init__(self):
        self.model = DataModel()  # Your model, which handles data fetching or other operations
        self.view = MainView(self)  # View that will be controlled by the controller

    def run(self):
        # Possibly fetch data from model (if needed) and display it via the view
        self.view.display_window()

    def on_submit(self, text_widget):
        # Fetch the text from the Text widget
        user_input = text_widget.get("1.0", "end-1c")  
        filtred_words = self.filter_words(user_input)  
        response = self.model.search_images(filtred_words)  # Call the model's search_images method with the filtered words
        print(len(response))  # Print the response
        self.save_images(response)
        
    def save_images(self, response):
        self.model.download_image(response)
        

    def filter_words(self, words):
        # Use regular expression to extract words between square brackets []
        pattern = re.compile(r"\[(\w+)\]", re.IGNORECASE)  # Match word characters inside []
        matches = pattern.findall(words)  # findall returns all matches
        return matches  # Return the list of filtered words

