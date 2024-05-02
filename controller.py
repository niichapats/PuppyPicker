""" Controller for Puppy Picker """

from view import PuppyPickerView
from model import PuppyPickerModel


class PuppyPickerController:
    """
    Controller for the Puppy Picker application.
    Handle user interactions between the PuppyPickerModel and PuppyPickerView.
    """
    def __init__(self):
        """
        Initialize the PuppyPickerController.
        Create instances of the PuppyPickerModel and PuppyPickerView, establishing the
        controller's connection with the model and view components.
        """
        self.model = PuppyPickerModel()
        self.view = PuppyPickerView(self)

    def next_button_handler(self, page):
        if page == 1:
            self.view.find_breeds_page2(self.model.descriptive_lifespan())

    def show_info_handler(self):
        print(self.view.user_preference('show_breed'))

    def run(self):
        """
        Run the program by running CalculatorView
        :return:
        """
        self.view.run()
