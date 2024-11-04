from views.main_view import MainView
from controllers.main_controller import MainController

if __name__ == "__main__":
    app = MainView()
    controller = MainController(app)
    app.run()
