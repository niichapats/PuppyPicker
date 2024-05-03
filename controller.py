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
        elif page == 2:
            self.view.run_find_breeds_page3()
        elif page == 3:
            prefer_list = self.view.get_user_prefer()
            allowed_values = {'0', '1', '2', '3', 'small', 'medium', 'big', 'all'}
            correct_value = True
            for item in prefer_list:
                if item not in allowed_values:
                    correct_value = False
            if '' in prefer_list:
                self.view.inform_error('Please complete all required fields')
            elif 'Select' in prefer_list:
                self.view.inform_error('Please choose a size')
            elif not correct_value:
                self.view.inform_error('Please enter only 0-3')
                self.view.clear_user_prefer()
            else:
                top_name, top_score = self.model.find_matching_breeds(prefer_list)
                print(top_name)
                print(top_score)
                self.view.find_breeds_page4(top_name, top_score)

    def show_info_handler(self):
        print(self.view.user_preference('show_breed'))

    def run(self):
        """
        Run the program by running CalculatorView
        :return:
        """
        self.view.run()
