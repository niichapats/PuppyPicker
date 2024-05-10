""" Controller for Puppy Picker """

from view import PuppyPickerView
from model import PuppyPickerModel
from graph_manage import GraphManage


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
        self.graph_manage = GraphManage()

    def next_button_handler(self, page):
        if page == 1:
            self.view.find_breeds_page2(self.model.descriptive_lifespan())
        elif page == 2:
            self.view.find_breeds_page3()
        elif page == 3:
            prefer_list = self.view.get_user_prefer()
            allowed_values = {'0', '1', '2', '3', 'small', 'medium', 'big', 'all'}
            correct_value = True
            for item in prefer_list:
                if item not in allowed_values:
                    correct_value = False
            if '' in prefer_list:
                self.view.report_error('Please complete all required fields')
            elif 'Select' in prefer_list:
                self.view.report_error('Please select a size')
            elif not correct_value:
                self.view.report_error('Please enter only 0-3')
            else:
                top_name, top_score = self.model.find_matching_breeds(prefer_list)
                self.view.find_breeds_page4(top_name, top_score)
        elif page == 4:
            if self.view.selected_breed_combo.get() != 'Select':
                self.view.dog_info_page()
            else:
                self.view.report_error('Please Select Dog Breed')

    def show_info_handler(self):
        if self.view.selected_breed_combo.get() != 'Select':
            self.view.dog_info_page()
        else:
            self.view.report_error('Please Select Dog Breed')

    def gender_combobox_handler(self, event):
        breed = self.view.selected_breed_combo.get()
        self.view.canvas_widget_gender.destroy()
        selected_gender = self.view.selected_gender_combo.get()
        if selected_gender == 'Male':
            self.view.draw_male_graph(breed)
        elif selected_gender == 'Female':
            self.view.draw_female_graph(breed)

    def ex_show_graph_handler(self):
        page = self.view.explore_page
        if self.view.selected1_explore.get() != 'Select Attribute (x)' \
                and self.view.selected2_explore.get() != 'Select Attribute (y)':
            if page == 'bar':
                self.view.draw_explore_bar()
            elif page == 'scatter':
                self.view.draw_explore_scatter()
            elif page == 'histogram':
                if self.view.selected1_explore.get() != 'Select Group' \
                        and self.view.selected2_explore.get() != 'Select Attribute':
                    self.view.draw_explore_hist()
                else:
                    self.view.report_error('Please Select attributes')
        else:
            self.view.report_error('Please Select attributes')

    def show_compare_handler(self):
        if self.view.selected1_breed_compare.get() != 'Select Dog Breed' \
                and self.view.selected2_breed_compare.get() != 'Select Dog Breed':
            self.view.draw_compare_graph()
        else:
            self.view.report_error('Please Select Dog Breed')

    def run(self):
        """
        Run the program by running CalculatorView
        :return:
        """
        self.view.run()
