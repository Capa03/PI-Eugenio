# src/controllers/main_controller.py
from models.data_model import DataModel
from views.main_view import MainView

# MainController class
# This class is responsible for controlling the flow of the application.
class MainController:
    def __init__(self):
        self.model = DataModel()
        self.view = MainView()

    def run(self):
        data = self.model.get_data()
        self.view.display_data(data)
