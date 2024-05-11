""" UI for Puppy Picker """

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph_manage import GraphManage


class PuppyPickerView(tk.Tk):
    """ Graphical user interface for Puppy Picker """

    def __init__(self, controller):
        """
        Initialize the CalculatorView.
        :param controller: An instance of the CalculatorController class
        to establish the connection between the view and the controller.
        """
        super().__init__()
        self.controller = controller
        self.title('Puppy Picker')
        self.minsize(width=1060, height=750)
        self.df = GraphManage.load_data('breeds.csv')
        self.graph_manage = GraphManage()
        # Find Matching Breed
        self.page_find_breeds = 0
        self.selected_story_combo = tk.StringVar()
        self.default_story_combo = 'Select Histogram'
        self.selected_story_combo.set(self.default_story_combo)
        self.selected_size = tk.StringVar()
        # Statistical Information
        self.selected_breed_combo = tk.StringVar()
        self.selected_gender_combo = tk.StringVar()
        # Data exploration
        self.explore_page = 0
        self.selected1_explore = tk.StringVar()
        self.selected2_explore = tk.StringVar()
        # Characteristic Comparison
        self.selected1_breed_compare = tk.StringVar()
        self.selected2_breed_compare = tk.StringVar()
        self.init_component()

    def init_component(self):
        """
        Initialize and set up GUI components.
        """

        # Define color scheme
        light_brown_bg = '#FFFAF0'
        white_bg = '#FFFAFA'
        light_brown_text = '#9C661F'
        brown_text = '#8B3626'

        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=light_brown_bg)

        style.configure('TLabel', background=light_brown_bg, foreground=light_brown_text,
                        font=('Times New Roman', 20))
        style.configure('Small.TLabel', background='white', foreground=light_brown_text,
                        font=('Times New Roman', 17))
        style.configure('Medium.TLabel', background=light_brown_bg, foreground=light_brown_text,
                        font=('Times New Roman', 18))
        style.configure('WhiteCenter.TLabel', anchor='center', background='white',
                        foreground=light_brown_text, font=('Times New Roman', 20),
                        padding=20)
        style.configure('Centered.TLabel', anchor='center', font=('Times New Roman', 20),
                        background='white', foreground='#9C661F', padding=20)

        style.configure('TButton', background=white_bg, foreground=light_brown_text,
                        font=('Times New Roman', 15))
        style.configure('TEntry', fieldbackground='white', foreground=brown_text)
        style.configure('Big.TButton', padding=[20, 10], font=('Times New Roman', 20))
        style.configure('Custom.TCombobox', foreground=light_brown_text, background='white')

        self.configure(bg='snow1')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create top frame
        self.top_frame = ttk.Frame(self, style='TFrame')
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Load and display the logo image
        image = Image.open('logo.png')
        image = image.resize((650, 120), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = ttk.Label(self.top_frame, image=photo)
        image_label.image = photo
        image_label.pack()

        self.menu_label = ttk.Label(self.top_frame, text="Let's Find Your Ideal Match!",
                                    style='TLabel', padding=(60, 0))
        self.menu_label.pack()

        # Create left and right frame
        self.left_frame = self.create_left_frame()
        self.left_frame.grid(row=1, column=0, sticky='nsew')
        self.create_nav_button()

        self.right_frame = self.create_right_frame_welcome()
        self.right_frame.grid(row=1, column=1, sticky='nsew', padx=(0, 20))

        # Create bottom frame
        self.bottom_frame = self.create_bottom_frame()
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')

    def create_left_frame(self):
        """
        Left Frame for Navigation Buttons
        """
        left_frame = ttk.Frame(self, width=400, padding=0, style='TFrame')
        return left_frame

    def create_right_frame_welcome(self):
        """
        The initial right frame welcoming the user and
        displaying introductory information.
        """
        right_frame = ttk.Frame(self, padding=5, style='TFrame')

        home_info = ttk.Label(right_frame,
                              text="Welcome !\n\nLet's explore breed traits "
                                   "through detailed graphs and \n\nfind your "
                                   "ideal match with personalized recommendations.",
                              style='WhiteCenter.TLabel')
        home_info.pack(fill="both", expand=True)
        return right_frame

    def create_bottom_frame(self):
        """
        Bottom frame containing exit button and next button
        """
        bottom_frame = ttk.Frame(self)
        exit_button = ttk.Button(bottom_frame, text="Exit", style='Big.TButton',
                                 cursor="heart", command=self.destroy)
        exit_button.pack(side=tk.LEFT, padx=35, pady=25)
        return bottom_frame

    def create_nav_button(self):
        """
        Create Navigation buttons
        """
        nav_buttons = ['Find Matching Breeds', 'Statistical Information',
                       'Characteristics Comparison']
        button_commands = [self.find_breeds_page1, self.statistical_page, self.comparison_page]

        for i, (text, command) in enumerate(zip(nav_buttons, button_commands)):
            button = ttk.Button(self.left_frame, text=text, style='Big.TButton',
                                cursor='heart', command=command)
            button.grid(row=i, column=0, sticky='ew', padx=30, pady=10)
            self.left_frame.grid_rowconfigure(i, weight=1)

    def clear_right_frame(self):
        """
        Clears all widgets in the right frame to prepare for new content.
        """
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def clear_default_text(self, event=None):
        """
        Clear default text on the combo box
        """
        current_value = self.selected_story_combo.get()
        if current_value == self.default_story_combo:
            self.selected_story_combo.set("")

    # Find Matching Breeds
    def find_breeds_page1(self):
        """
        Displays the first page for the "Find Matching Breeds" menu
        """
        self.page_find_breeds = 1
        self.menu_label.destroy()
        try:
            self.next_button.destroy()
        except AttributeError:
            pass
        self.clear_right_frame()

        self.menu_label = ttk.Label(self.top_frame, text='Find Matching Breeds',
                                    style='TLabel', padding=(60, 0))
        self.menu_label.pack()

        menu_info = ttk.Label(self.right_frame,
                              text="   Choose size of a dog you prefer and rate "
                                   "the importance you place on   \n\n"
                                   "   each characteristic when considering "
                                   "getting a dog.   \n\n\n\n"
                                   "   Before Finding your matching breeds,    \n\n"
                                   "   let’s see some interesting story    ",
                              style='WhiteCenter.TLabel')
        menu_info.pack(fill='both', expand=True)
        self.next_button = ttk.Button(self.bottom_frame, text="Next",
                                      style='Big.TButton', cursor="heart",
                                      command=lambda: self.controller.next_button_handler(self.page_find_breeds))
        self.next_button.pack(side=tk.RIGHT, padx=35, pady=25)

    def find_breeds_page2(self, data):
        """
        Displays the second page of the "Find Matching Breeds" menu
        which includes the storytelling
        """
        self.page_find_breeds = 2
        self.clear_right_frame()

        # Top sub frame for label 1 ,graph 1 and graph 2
        self.top_sub_frame = tk.Frame(self.right_frame, background='white')
        self.top_sub_frame.pack(side="top", fill="both", expand=True)

        # Label 1: descriptive statistic
        descriptive_stat = ttk.Label(self.top_sub_frame,
                                     text=f'Descriptive Statistic\n'
                                          f'-----------------------\n'
                                          f'Average Lifespan\n'
                                          f'Min: {data[0]}\n'
                                          f'Max: {data[1]}\n'
                                          f'Mean: {data[2]}\n'
                                          f'Mode: {data[3]}',
                                     style='Small.TLabel')
        descriptive_stat.pack(side="right", fill="both", expand=True, padx=15)

        # Top left sub frame for combo box and graph 2
        self.story_top_left_frame = tk.Frame(self.top_sub_frame, background='white')
        self.story_top_left_frame.pack(side="left", fill="both", expand=True)

        # Combo box for selecting histogram
        story_hist_list = ['max_life_expectancy', 'max_height_male',
                           'max_height_female', 'max_weight_male',
                           'max_weight_female']
        story_combobox = ttk.Combobox(self.story_top_left_frame,
                                      textvariable=self.selected_story_combo,
                                      values=story_hist_list, state="readonly",
                                      style='Custom.TCombobox')
        story_combobox.pack(side="top", fill="x", expand=False, padx=(20, 40), pady=(5, 0))
        story_combobox.bind('<<ComboboxSelected>>', self.story_combobox_handler)

        # Graph 1: default histogram
        self.story_hist = self.graph_manage.create_histogram('max_life_expectancy', 'small')
        canvas = FigureCanvasTkAgg(self.story_hist, master=self.story_top_left_frame)
        canvas.draw()
        self.canvas_widget_story = canvas.get_tk_widget()
        self.canvas_widget_story.config(width=240, height=210)
        self.canvas_widget_story.pack(side="top", fill="both", expand=True, padx=(20, 40))

        # Graph 2: Bar graph represent size and lifespan
        fig_bar = self.graph_manage.story_bar()
        canvas = FigureCanvasTkAgg(fig_bar, master=self.top_sub_frame)
        canvas_widget_bar = canvas.get_tk_widget()
        canvas_widget_bar.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # Middle sub frame for Graph 3 and Graph 4
        self.story_middle_frame = tk.Frame(self.right_frame)
        self.story_middle_frame.pack(side="top", fill="both", expand=True)

        # Graph 3: scatter plot
        story_scatter = self.graph_manage.story_scatter()
        canvas = FigureCanvasTkAgg(story_scatter, master=self.story_middle_frame)
        canvas_widget_heatmap = canvas.get_tk_widget()
        canvas_widget_heatmap.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # Graph 4: correlation heat map
        story_heatmap = self.graph_manage.story_heatmap()
        canvas = FigureCanvasTkAgg(story_heatmap, master=self.story_middle_frame)
        canvas_widget_heatmap = canvas.get_tk_widget()
        canvas_widget_heatmap.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # Bottom sub frame for label 2
        story_bottom_frame = tk.Frame(self.right_frame)
        story_bottom_frame.pack(side="top", fill="x", expand=False)

        # Label 2: summary of the storytelling
        summary = ttk.Label(story_bottom_frame,
                            text='Our data highlights a trend: larger dogs '
                                 'often have shorter lifespans.\n'
                                 'Please consider this when selecting your new puppy.',
                            style='Small.TLabel')
        summary.pack(side="top", fill="both", expand=True)

    def story_combobox_handler(self, event):
        """
        Handle combobox selection in second page of "Find Matching Breeds" menu.
        """
        selected_var = self.selected_story_combo.get()
        if selected_var != self.default_story_combo:
            self.update_hist(selected_var)

    def update_hist(self, selected_var):
        """
        Update the histogram in the storytelling section
        by retrieving data from a combobox.
        """
        self.canvas_widget_story.destroy()
        self.story_hist = self.graph_manage.create_histogram(selected_var, 'small')
        canvas = FigureCanvasTkAgg(self.story_hist, master=self.story_top_left_frame)
        canvas.draw()
        self.canvas_widget_story = canvas.get_tk_widget()
        self.canvas_widget_story.config(width=240, height=210)
        self.canvas_widget_story.pack(fill=tk.BOTH, expand=True, padx=(20, 70))

    def find_breeds_page3(self):
        """
        Displays the third page of the "Find Matching Breeds" menu.

        This page allows users to input their preferences for
        dog characteristics to assist in finding matching dog breeds.
        """
        self.clear_right_frame()
        self.page_find_breeds = 3
        top_label = ttk.Label(self.right_frame, style='TLabel',
                              text="Each characteristic is rated from 0 to 3, "
                                   "where 1 indicates low importance,\n\n"
                                   "3 indicates high importance, and 0 means "
                                   "you are not interested in that trait.",)
        top_label.pack(side="top", padx=10, pady=40)

        # Create frames for left and right columns
        left_frame = ttk.Frame(self.right_frame, style='TFrame')
        right_frame = ttk.Frame(self.right_frame, style='TFrame')
        left_frame.pack(side="left", fill="y", expand=True, padx=10, pady=10)
        right_frame.pack(side="right", fill="y", expand=True, padx=10, pady=10)

        # Left sub frame
        label1_widget = ttk.Label(left_frame, text='Adaptability\n\n\n'
                                                   'Friendliness\n\n\n'
                                                   'Health grooming\n\n\n'
                                                   'Trainability',
                                  style='TLabel', padding=10)
        label1_widget.pack(side="left", anchor='n')

        self.entry_adapt = ttk.Entry(left_frame, width=10, style='TEntry')
        self.entry_adapt.pack(side="top", anchor='ne', padx=20, pady=(15, 25))

        self.entry_friendly = ttk.Entry(left_frame, width=10, style='TEntry')
        self.entry_friendly.pack(side="top", anchor='ne', padx=20, pady=(20, 25))

        self.entry_health = ttk.Entry(left_frame, width=10, style='TEntry')
        self.entry_health.pack(side="top", anchor='ne', padx=20, pady=(20, 25))

        self.entry_train = ttk.Entry(left_frame, width=10, style='TEntry')
        self.entry_train.pack(side="top", anchor='ne', padx=20, pady=(20, 25))

        # right sub frame
        label2_widget = ttk.Label(right_frame, text='Exercise needs\n\n\n'
                                                    'Long lifespan\n\n\n'
                                                    'Size',
                                  style='TLabel', padding=10)
        label2_widget.pack(side="left", anchor='n')

        self.entry_exercise = ttk.Entry(right_frame, width=10, style='TEntry')
        self.entry_exercise.pack(side="top", anchor='ne', padx=20, pady=(20, 25))

        self.entry_life = ttk.Entry(right_frame, width=10, style='TEntry')
        self.entry_life.pack(side="top", anchor='ne', padx=20, pady=(20, 25))

        size_list = ['all', 'small', 'medium', 'big']
        size_combobox = ttk.Combobox(right_frame, textvariable=self.selected_size, values=size_list,
                                     width=10, state='readonly', style='Custom.TCombobox')
        size_combobox.pack(side="top", anchor='ne', padx=20, pady=(20, 25))
        size_combobox.set('Select')

    def find_breeds_page4(self, name_list, score_list):
        """
        Displays the fourth page of the "Find Matching Breeds" menu.

        This page presents a list of matching dog breeds based on
        user preferences, scored and sorted by relevance.
        It allows users to select from these breeds to
        view more detailed information about each one.
        """
        self.clear_right_frame()
        self.page_find_breeds = 4

        # Create frames for left and right columns
        left_frame = ttk.Frame(self.right_frame, style='TFrame')
        right_frame = ttk.Frame(self.right_frame, style='TFrame')
        left_frame.pack(side="left", fill="y", expand=True, padx=10, pady=10)
        right_frame.pack(side="right", fill="y", expand=True, padx=10, pady=10)

        score_graph = self.graph_manage.score_bar(name_list, score_list)
        canvas = FigureCanvasTkAgg(score_graph, master=left_frame)
        canvas_widget_score = canvas.get_tk_widget()
        canvas_widget_score.pack(side="left", expand=True)
        canvas.draw()

        best_match = ttk.Label(right_frame, text=f'Your Best Match\n\n'
                                                 f': {name_list[0]}\n\n\n\n\n\n\n'
                                                 f'Select breed\n\n'
                                                 f'to see more information')
        best_match.pack(padx=10, expand=True)

        self.combobox_breed1 = ttk.Combobox(right_frame, textvariable=self.selected_breed_combo,
                                            values=name_list, state='readonly',
                                            style='Custom.TCombobox')
        self.combobox_breed1.pack(anchor='n', padx=10, expand=True)
        self.combobox_breed1.set('Select')

    def get_user_prefer(self):
        """
        Collects and returns the user's preferences from input fields.
        Gathers inputs for dog traits and size from the GUI and returns them as a list.
        """
        prefer_list = [self.entry_adapt.get(), self.entry_friendly.get(), self.entry_health.get(),
                       self.entry_train.get(), self.entry_exercise.get(), self.entry_life.get(),
                       self.selected_size.get()]
        return prefer_list

    # Statistical Information
    def statistical_page(self):
        """
        Displays the third page of the "Statistical Information" menu.

        This page allows users to select dog breeds and explore their statistics.
        It includes buttons for choosing breeds to show detailed information
        and options for further data exploration.
        """

        self.menu_label.destroy()
        try:
            self.next_button.destroy()
        except AttributeError:
            pass
        self.clear_right_frame()

        sorted_df = self.df.sort_values(by='breed')
        sorted_breed_list = sorted_df['breed'].tolist()

        self.menu_label = ttk.Label(self.top_frame, text='Statistical Information',
                                    style='TLabel', padding=(55, 0))
        self.menu_label.pack()

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, minsize=50)
        self.right_frame.grid_rowconfigure(1, minsize=50)
        self.right_frame.grid_rowconfigure(2, minsize=50)
        self.right_frame.grid_rowconfigure(3, minsize=100)
        self.right_frame.grid_rowconfigure(4, minsize=70)

        # Label and combobox for choosing a breed
        self.label_choose_breed = ttk.Label(self.right_frame,
                                            text='Select dog breed', style='TLabel')
        self.label_choose_breed.grid(row=0, column=0, padx=170, pady=(70, 0), sticky='ew')
        self.combobox_breed2 = ttk.Combobox(self.right_frame, width=30,
                                            textvariable=self.selected_breed_combo,
                                            values=sorted_breed_list, state='readonly',
                                            style='Custom.TCombobox')
        self.combobox_breed2.grid(row=1, column=0, padx=170, pady=(20, 0), sticky='ew')
        self.combobox_breed2.set('Select')

        # Button to show information
        self.show_info_button = ttk.Button(self.right_frame, text='Show Information',
                                           style='TButton',
                                           cursor='heart',
                                           command=self.controller.show_info_handler)
        self.show_info_button.grid(row=2, column=0, padx=170, pady=20, sticky='ew')

        # Label for data exploration section
        self.explore_label = ttk.Label(self.right_frame,
                                       text='Data exploration\n\n'
                                            'Select attributes and plot your own graph',
                                       style='TLabel')
        self.explore_label.grid(row=3, column=0, padx=170, pady=0, sticky='ew')

        # Button for exploring data
        self.explore_button = ttk.Button(self.right_frame, text='Explore', style='TButton',
                                         cursor='heart', command=self.data_exploration_page)
        self.explore_button.grid(row=4, column=0, padx=170, pady=0, sticky='new')

    def dog_info_page(self):
        """
        Displays detailed information about a selected dog breed on the breed information page.

        This page allows users to view characteristics such as breed group, size, lifespan,
        and to select a gender for additional specific details.
        """
        self.clear_right_frame()
        try:
            self.next_button.destroy()
        except AttributeError:
            pass
        self.clear_right_frame()

        breed = self.selected_breed_combo.get()
        breed_group = self.df[self.df['breed'] == breed]['breed_group'].iloc[0]
        breed_size = self.df[self.df['breed'] == breed]['size_category'].iloc[0]
        min_lifespan = self.df[self.df['breed'] == breed]['min_life_expectancy'].iloc[0]
        max_lifespan = self.df[self.df['breed'] == breed]['max_life_expectancy'].iloc[0]

        self.info_left_frame = ttk.Frame(self.right_frame, style='TFrame')
        right_frame = ttk.Frame(self.right_frame, style='TFrame')
        self.info_left_frame.pack(side='left', fill='y', expand=True, padx=10, pady=10)
        right_frame.pack(side='right', fill='y', expand=True, padx=10, pady=10)

        # Left sub frame
        breed_label = ttk.Label(self.info_left_frame, text=f'[ {breed} ]', style='TLabel')
        breed_label.pack(side='top', pady=(20, 0), expand=True)

        gender_combobox = ttk.Combobox(self.info_left_frame,
                                       textvariable=self.selected_gender_combo,
                                       values=['Male', 'Female'], state='readonly',
                                       style='Custom.TCombobox')
        gender_combobox.pack(side='top', pady=10, expand=True)
        gender_combobox.set('Select Gender')
        gender_combobox.bind('<<ComboboxSelected>>', self.controller.gender_combobox_handler)

        # Default gender graph (Male)
        self.draw_male_graph(breed)

        # Right sub frame
        info_label = ttk.Label(right_frame, text=f'Breed Group: {breed_group}         Size: {breed_size}\n\n'
                                                 f'Min Lifespan: {min_lifespan}         Max Lifespan: {max_lifespan}',
                               style='Medium.TLabel')
        info_label.pack(expand=True, pady=10)

        char_bar = self.graph_manage.char_bar(breed)
        canvas = FigureCanvasTkAgg(char_bar, master=right_frame)
        canvas_widget_score = canvas.get_tk_widget()
        canvas_widget_score.pack(side='top', anchor='n', expand=True)
        canvas.draw()

    def draw_male_graph(self, breed):
        """
        Draws a graph displaying the height and weight statistics
        for male dogs of a selected breed.
        """
        gender_bar = self.graph_manage.male_bar(breed)
        canvas = FigureCanvasTkAgg(gender_bar, master=self.info_left_frame)
        self.canvas_widget_gender = canvas.get_tk_widget()
        self.canvas_widget_gender.pack(side='top', pady=10, anchor='n', expand=True)
        canvas.draw()

    def draw_female_graph(self, breed):
        """
        Draws a graph displaying the height and weight statistics
        for female dogs of a selected breed.
        """
        gender_bar = self.graph_manage.female_bar(breed)
        canvas = FigureCanvasTkAgg(gender_bar, master=self.info_left_frame)
        self.canvas_widget_gender = canvas.get_tk_widget()
        self.canvas_widget_gender.pack(side='top', pady=10, anchor='n', expand=True)
        canvas.draw()

    # Data Exploration
    def data_exploration_page(self):
        """
        Displays the data exploration page.

        On this page, users can choose from various attributes to plot custom graphs
        """
        self.clear_right_frame()
        top_frame_explore = ttk.Frame(self.right_frame, style='TFrame')
        self.middle_frame_explore = ttk.Frame(self.right_frame, style='TFrame')
        self.bottom_frame_explore = ttk.Frame(self.right_frame, style='TFrame')

        top_frame_explore.pack(side='top', fill='x')
        self.middle_frame_explore.pack(side='top', fill='both', expand=True)
        self.bottom_frame_explore.pack(side='top', fill='both', expand=True)

        ex_bar_button = ttk.Button(top_frame_explore, text='Bar Graph', style='TButton',
                                   cursor='heart', command=self.explore_bar_page)
        ex_bar_button.pack(side='left', anchor='nw', padx=(100, 15), pady=50, expand=True)

        ex_scatter_button = ttk.Button(top_frame_explore, text='Scatter Plot', style='TButton'
                                       , cursor='heart', command=self.explore_scatter_page)
        ex_scatter_button.pack(side='left', anchor='nw', padx=15, pady=50, expand=True)

        ex_scatter_button = ttk.Button(top_frame_explore, text='Histogram', style='TButton'
                                       , cursor='heart', command=self.explore_hist_page)
        ex_scatter_button.pack(side='left', anchor='nw', padx=15, pady=50, expand=True)

        show_graph_button = ttk.Button(top_frame_explore, text='Show Graph',
                                       style='TButton', cursor='heart',
                                       command=self.controller.ex_show_graph_handler)
        show_graph_button.pack(side='left', anchor='nw', padx=(100, 0), pady=50, expand=True)

        self.explore_bar_page()

    def explore_bar_page(self):
        """
        The interface for plotting bar graphs on the data exploration page.
        """
        self.explore_page = 'bar'
        for widget in self.bottom_frame_explore.winfo_children():
            widget.destroy()
        for widget in self.middle_frame_explore.winfo_children():
            widget.destroy()
        # Attribute 1
        bar_list1 = ['breed_group', 'size_category']
        bar_combobox1 = ttk.Combobox(self.middle_frame_explore, textvariable=self.selected1_explore,
                                     values=bar_list1, state='readonly', style='Custom.TCombobox')
        bar_combobox1.pack(side='left', anchor='ne', padx=30, expand=True)
        bar_combobox1.set('Select Attribute (x)')

        # Attribute 2
        bar_list2 = ['adaptability', 'all_around_friendliness', 'health_grooming', 'trainability',
                     'exercise_needs', 'average_lifespan']
        bar_combobox2 = ttk.Combobox(self.middle_frame_explore, textvariable=self.selected2_explore,
                                     values=bar_list2, state='readonly', style='Custom.TCombobox')
        bar_combobox2.pack(side='left', anchor='nw', padx=30, expand=True)
        bar_combobox2.set('Select Attribute (y)')

        # Default graph
        default = self.graph_manage.explore_bar('breed_group', 'adaptability')
        canvas = FigureCanvasTkAgg(default, master=self.bottom_frame_explore)
        canvas_widget_test = canvas.get_tk_widget()
        canvas_widget_test.pack(side='top', anchor='n', pady=20, expand=True)
        canvas.draw()

    def explore_scatter_page(self):
        """
        The interface for plotting scatter plot on the data exploration page.
        """
        self.explore_page = 'scatter'
        for widget in self.bottom_frame_explore.winfo_children():
            widget.destroy()
        for widget in self.middle_frame_explore.winfo_children():
            widget.destroy()
        # Attribute 1
        scatter_list1 = ['max_height_male', 'max_height_female',
                         'max_weight_male', 'max_weight_female',
                         'average_lifespan', 'average_size']
        bar_combobox1 = ttk.Combobox(self.middle_frame_explore,
                                     textvariable=self.selected1_explore,
                                     values=scatter_list1, state='readonly',
                                     style='Custom.TCombobox')
        bar_combobox1.pack(side='left', anchor='ne', padx=30, expand=True)
        bar_combobox1.set('Select Attribute (x)')

        # Attribute 2
        scatter_list2 = ['max_height_male', 'max_height_female',
                         'max_weight_male', 'max_weight_female',
                         'average_lifespan', 'average_size']
        bar_combobox2 = ttk.Combobox(self.middle_frame_explore,
                                     textvariable=self.selected2_explore,
                                     values=scatter_list2, state='readonly',
                                     style='Custom.TCombobox')
        bar_combobox2.pack(side='left', anchor='nw', padx=30, expand=True)
        bar_combobox2.set('Select Attribute (y)')

        # Default graph
        default = self.graph_manage.explore_scatter('max_height_male', 'average_lifespan')
        canvas = FigureCanvasTkAgg(default, master=self.bottom_frame_explore)
        canvas_widget_test = canvas.get_tk_widget()
        canvas_widget_test.pack(side='top', anchor='n', pady=20, expand=True)
        canvas.draw()

    def explore_hist_page(self):
        """
        The interface for plotting histogram on the data exploration page.
        """
        self.explore_page = 'histogram'
        for widget in self.bottom_frame_explore.winfo_children():
            widget.destroy()
        for widget in self.middle_frame_explore.winfo_children():
            widget.destroy()
        hist_list1 = ['all', 'Sporting Dogs', 'Hound Dogs', 'Working Dogs',
                      'Companion Dogs', 'Herding Dogs', 'Terrier Dogs']
        bar_combobox1 = ttk.Combobox(self.middle_frame_explore,
                                     textvariable=self.selected1_explore,
                                     values=hist_list1, state='readonly',
                                     style='Custom.TCombobox')
        bar_combobox1.pack(side='left', anchor='ne', padx=30, expand=True)
        bar_combobox1.set('Select Group')

        # Attribute 2
        hist_list2 = ['max_height_male', 'max_height_female',
                      'max_weight_male', 'max_weight_female',
                      'average_lifespan', 'average_size', 'adaptability', 'all_around_friendliness',
                      'health_grooming', 'trainability', 'exercise_needs', 'average_lifespan']
        bar_combobox2 = ttk.Combobox(self.middle_frame_explore, textvariable=self.selected2_explore,
                                     values=hist_list2, state='readonly', style='Custom.TCombobox')
        bar_combobox2.pack(side='left', anchor='nw', padx=30, expand=True)
        bar_combobox2.set('Select Attribute')

        # Default graph
        default = self.graph_manage.create_histogram('max_height_male', 'big')
        canvas = FigureCanvasTkAgg(default, master=self.bottom_frame_explore)
        canvas_widget_test = canvas.get_tk_widget()
        canvas_widget_test.pack(side='top', anchor='n', pady=20, expand=True)
        canvas.draw()

    def draw_explore_bar(self):
        """
        Draws a bar graph based on selected attributes for the data exploration page.
        """
        for widget in self.bottom_frame_explore.winfo_children():
            widget.destroy()
        explore_bar = self.graph_manage.explore_bar(self.selected1_explore.get(),
                                                    self.selected2_explore.get())
        canvas = FigureCanvasTkAgg(explore_bar, master=self.bottom_frame_explore)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side='top', anchor='n', pady=20, expand=True)
        canvas.draw()

    def draw_explore_scatter(self):
        """
        Draws a scatter plot based on selected attributes for the data exploration page.
        """
        for widget in self.bottom_frame_explore.winfo_children():
            widget.destroy()
        explore_scatter = self.graph_manage.explore_scatter(self.selected1_explore.get(),
                                                            self.selected2_explore.get())
        canvas = FigureCanvasTkAgg(explore_scatter, master=self.bottom_frame_explore)
        canvas_widget_test = canvas.get_tk_widget()
        canvas_widget_test.pack(side='top', anchor='n', pady=20, expand=True)
        canvas.draw()

    def draw_explore_hist(self):
        """
        Draws a histogram based on selected attributes for the data exploration page.
        """
        for widget in self.bottom_frame_explore.winfo_children():
            widget.destroy()
        selected_group = self.selected1_explore.get()
        if selected_group == 'all':
            explore_hist = self.graph_manage.create_histogram(self.selected2_explore.get(), 'big')
            canvas = FigureCanvasTkAgg(explore_hist, master=self.bottom_frame_explore)
            canvas_widget_test = canvas.get_tk_widget()
            canvas_widget_test.pack(side='top', anchor='n', pady=20, expand=True)
            canvas.draw()
        else:
            explore_hist = self.graph_manage.explore_breed_group_histgram(self.selected1_explore.get(),
                                                                          self.selected2_explore.get())
            canvas = FigureCanvasTkAgg(explore_hist, master=self.bottom_frame_explore)
            canvas_widget_test = canvas.get_tk_widget()
            canvas_widget_test.pack(side='top', anchor='n', pady=20, expand=True)
            canvas.draw()

    # Characteristic Comparison
    def comparison_page(self):
        """
        Displays a page for comparing the characteristics of two selected
        dog breeds using a multiple bar graph.
        """
        self.menu_label.destroy()
        try:
            self.next_button.destroy()
        except AttributeError:
            pass
        self.clear_right_frame()
        self.menu_label = ttk.Label(self.top_frame, text="Characteristics Comparison",
                                    style='TLabel', padding=(45, 0))
        self.menu_label.pack()

        top_frame_compare = ttk.Frame(self.right_frame, style='TFrame')
        top_frame_compare.pack(side='top', fill='both', expand=True)
        self.bottom_frame_compare = ttk.Frame(self.right_frame, style='TFrame')
        self.bottom_frame_compare.pack(side='top', fill='both', expand=True)

        sorted_df = self.df.sort_values(by='breed')
        sorted_breed_list = sorted_df['breed'].tolist()
        self.combobox_breed_cp1 = ttk.Combobox(top_frame_compare, width=20,
                                               textvariable=self.selected1_breed_compare,
                                               values=sorted_breed_list, state='readonly',
                                               style='Custom.TCombobox')
        self.combobox_breed_cp1.pack(side='left', anchor='ne', padx=10, pady=70, expand=True)

        self.combobox_breed_cp2 = ttk.Combobox(top_frame_compare, width=20,
                                               textvariable=self.selected2_breed_compare,
                                               values=sorted_breed_list, state='readonly',
                                               style='Custom.TCombobox')
        self.combobox_breed_cp2.pack(side='left', anchor='nw', padx=10, pady=70, expand=True)

        self.compare_button = ttk.Button(top_frame_compare, text='Show Comparison', cursor='heart',
                                         command=self.controller.show_compare_handler)
        self.compare_button.pack(side='left', anchor='nw', padx=(30, 0), pady=65, expand=True)
        self.combobox_breed_cp1.set('Select Dog Breed')
        self.combobox_breed_cp2.set('Select Dog Breed')

        compare_list = ['all_around_friendliness', 'trainability',
                        'health_grooming', 'exercise_needs', 'adaptability']
        # Default graph
        char_compare_bar = self.graph_manage.compare_bar('Chihuahua',
                                                         'Golden Retriever', compare_list)
        canvas = FigureCanvasTkAgg(char_compare_bar, master=self.bottom_frame_compare)
        canvas_widget_test = canvas.get_tk_widget()
        canvas_widget_test.pack(side='top', anchor='n', expand=True)
        canvas.draw()

    def draw_compare_graph(self):
        """
        Draws a multiple bar graph comparing the characteristics of two selected dog breeds.
        """
        for widget in self.bottom_frame_compare.winfo_children():
            widget.destroy()
        compare_list = ['all_around_friendliness', 'trainability',
                        'health_grooming', 'exercise_needs', 'adaptability']
        breed1 = self.combobox_breed_cp1.get()
        breed2 = self.combobox_breed_cp2.get()
        char_compare_bar = self.graph_manage.compare_bar(breed1, breed2, compare_list)
        canvas = FigureCanvasTkAgg(char_compare_bar, master=self.bottom_frame_compare)
        canvas_widget_test = canvas.get_tk_widget()
        canvas_widget_test.pack(side='top', anchor='n', expand=True)
        canvas.draw()

    def report_error(self, inform_text):
        """
        Displays an error message in red text at the bottom right of the screen.
        """
        try:
            self.error.destroy()
        except AttributeError:
            pass
        self.error = ttk.Label(self.bottom_frame, text=inform_text,
                               background='#FFFAF0', foreground='red',
                               font=('Times New Roman', 22))
        self.error.pack(side='left', anchor='e', padx=60, expand=True)
        self.after(2000, self.error.destroy)

    def run(self):
        """
        Starts the tkinter main event loop to run the application.
        """
        self.mainloop()
