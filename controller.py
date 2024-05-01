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

    def show_info_handler(self):
        print(self.view.user_preference('show_breed'))

    # def histogram(self):
    #     self.df = load_data('path_to_breeds.csv')

    def run(self):
        """
        Run the program by running CalculatorView
        :return:
        """
        self.view.run()
