import re
from models.data_model import DataModel
from views.main_view import MainView


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
            self.view.show_error("Text input and keyboard name cannot be empty.")
            return

        try:
            word_matrix = self._extract_words_from_input(user_input)
            if not word_matrix:
                self.view.show_error("No valid words found in the input. Ensure words are in brackets [ ].")
                return

            self.model.search_and_process_images(word_matrix, keyboard_name)
        except Exception as e:
            self.view.show_error(f"An unexpected error occurred: {e}")

    def _extract_words_from_input(self, input_text):
        """
        Filtra e organiza palavras dentro de colchetes em uma matriz de linhas.
        """
        lines = input_text.splitlines()
        word_matrix = []

        for line in lines:
            words_in_line = re.findall(r"\[(\w+)\]", line)
            if words_in_line:
                word_matrix.append(words_in_line)

        return word_matrix
