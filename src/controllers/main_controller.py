import re
from models.data_model import DataModel
from views.main_view import MainView
from utils import enum_type

class MainController:
    def __init__(self):
        self.model = DataModel()
        self.view = MainView(self)

    def run(self):
        self.view.display_window()

    def on_submit(self, user_input, keyboard_name):
        """
        Processa a entrada do usuário e aciona a lógica de negócio.
        """
        if not user_input or not keyboard_name:
            self.view.show_error(enum_type.Message.ERROR, "Text input and keyboard name cannot be empty.")
            return

        try:
            print(user_input)
            word_matrix = self._extract_words_from_input(user_input)
            if not word_matrix:
                self.view.show_error(enum_type.Message.ERROR, "No valid words found in the input. Ensure words are in brackets [ ].")
                return

            self.model.search_and_process_images(word_matrix, keyboard_name)
        except Exception as e:
            self.view.show_error(enum_type.Message.ERROR, f"An unexpected error occurred: {e}")
            return        
        self.view.show_error(enum_type.Message.SUCCESS, f"Keyboard created with the words: {user_input}")

    def on_edit(self, file_path):
        """
        Handles the edit request by calling the model's edit functionality.
        """
        try:
            edited_content = self.model._read_file(file_path)
            self.view._edit_text(edited_content)
        except Exception as e:
            self.view.show_error(enum_type.Message.ERROR, f"Failed to edit file: {e}")
    


    def _extract_words_from_input(self, input_text):
        """
        Filters and organizes words inside brackets into a matrix of lines.
        """

        lines = input_text.splitlines()
        word_matrix = []

        for line in lines:
            if line:
                word_matrix.append(line)
            
        return word_matrix
