""" UI for Puppy Picker """

import tkinter as tk
import time
from threading import Thread
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph_manage import GraphManage


class PuppyPickerView(tk.Tk):
    """ Graphical user interface for the Calculator application. """

    def __init__(self, controller):
        """
        Initialize the CalculatorView.
        :param controller: An instance of the CalculatorController class
        to establish the connection between the view and the controller.
        """
        super().__init__()
        self.controller = controller
        self.title('Puppy Picker')
        self.minsize(width=1050, height=750)
        self.df = GraphManage.load_data('breeds.csv')

        self.page_find_breeds = 0
        self.selected_story_hist = tk.StringVar()
        self.default_story_combo = 'Select Histogram'

        self.selected_story_hist.set(self.default_story_combo)
        self.selected_size = tk.StringVar()

        self.selected_breed_combo = tk.StringVar()
        # self.selected_breed_combo2 = tk.StringVar()
        self.init_component()

    def init_component(self):
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

        self.right_frame = self.create_right_frame()
        self.right_frame.grid(row=1, column=1, sticky='nsew', pady=(10, 0), padx=(0, 20))

        # Create bottom frame
        self.bottom_frame = self.create_bottom_frame()
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')

    def create_left_frame(self):
        """
        Left Frame for Navigation Buttons
        """
        left_frame = ttk.Frame(self, width=400, padding=0, style='TFrame')
        return left_frame

    def create_right_frame(self):
        right_frame = ttk.Frame(self, padding=5, style='TFrame')

        home_info = ttk.Label(right_frame,
                              text="Welcome !\n\nLet's explore breed traits through detailed graphs and \n\nfind your ideal match with personalized recommendations.",
                              style='WhiteCenter.TLabel')
        home_info.pack(fill="both", expand=True)
        return right_frame

    def create_bottom_frame(self):
        """
        Bottom frame for exit button, next button
        """
        bottom_frame = ttk.Frame(self)
        exit_button = ttk.Button(bottom_frame, text="Exit", style='Big.TButton', cursor="heart", command=self.destroy)
        exit_button.pack(side=tk.LEFT, padx=35, pady=25)
        return bottom_frame

    def create_nav_button(self):
        """
        Create Navigation buttons
        """
        nav_buttons = ['Find Matching Breeds', 'Statistical Information', 'Characteristics Comparison']
        button_commands = [self.find_breeds_page1, self.statistical_page1, self.comparison_page1]

        for i, (text, command) in enumerate(zip(nav_buttons, button_commands)):
            button = ttk.Button(self.left_frame, text=text, style='Big.TButton', cursor="heart", command=command)
            button.grid(row=i, column=0, sticky='ew', padx=30, pady=10)
            self.left_frame.grid_rowconfigure(i, weight=1)

    def clear_right_frame(self):
        """
        Clear right frame for changing page
        """
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def clear_default_text(self, event=None):
        """
        Clear default text on the combo box
        """
        current_value = self.selected_story_hist.get()
        if current_value == self.default_story_combo:
            self.selected_story_hist.set("")

    # Find Matching Breeds
    # Page 1
    def find_breeds_page1(self):
        self.page_find_breeds = 1
        self.menu_label.destroy()
        try:
            self.next_button.destroy()
        except AttributeError:
            pass
        self.clear_right_frame()

        self.menu_label = ttk.Label(self.top_frame, text='Find Matching Breeds', style='TLabel', padding=(60, 0))
        self.menu_label.pack()

        menu_info = ttk.Label(self.right_frame,
                              text="   Choose size of a dog you prefer and rate the importance you place on   \n\n"
                                   "   each characteristic when considering getting a dog.   \n\n\n\n"
                                   "   Before Finding your matching breeds,    \n\n"
                                   "   let’s see some interesting story    ",
                              style='WhiteCenter.TLabel')
        menu_info.pack(fill='both', expand=True)
        self.next_button = ttk.Button(self.bottom_frame, text="Next", style='Big.TButton', cursor="heart",
                                      command=lambda: self.controller.next_button_handler(self.page_find_breeds))
        self.next_button.pack(side=tk.RIGHT, padx=35, pady=25)

    # Page 2
    def find_breeds_page2(self, data):
        self.page_find_breeds = 2
        self.clear_right_frame()

        # Top sub frame for label 1 and graph 1
        self.top_sub_frame = tk.Frame(self.right_frame, background='white')
        self.top_sub_frame.pack(side="top", fill="x", expand=False)

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
        descriptive_stat.pack(side="left", fill="both", expand=True, padx=10)

        # Graph 1: Bar graph represent size and lifespan
        fig_bar = GraphManage.story_bar(self.df)
        canvas = FigureCanvasTkAgg(fig_bar, master=self.top_sub_frame)
        canvas_widget_bar = canvas.get_tk_widget()
        canvas_widget_bar.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # Top right sub frame for combo box and graph 2
        self.story_top_right_frame = tk.Frame(self.top_sub_frame, background='white')
        self.story_top_right_frame.pack(side="left", fill="both", expand=True)

        # Combo box for selecting histogram
        story_hist_list = ['max_life_expectancy', 'max_height_male', 'max_height_female', 'max_weight_male',
                           'max_weight_female']
        story_combobox = ttk.Combobox(self.story_top_right_frame, textvariable=self.selected_story_hist,
                                      values=story_hist_list, state="readonly", style='Custom.TCombobox')
        story_combobox.pack(side="top", fill="x", expand=False, padx=(20, 70))
        story_combobox.bind('<<ComboboxSelected>>', self.story_combobox_handler)

        # Graph 2: default histogram
        self.story_hist = GraphManage.create_histogram(self.df, 'max_life_expectancy')
        canvas = FigureCanvasTkAgg(self.story_hist, master=self.story_top_right_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.config(width=240, height=210)
        self.canvas_widget.pack(side="top", fill="both", expand=True, padx=(20, 70))

        # Middle sub frame for Graph 3 and Graph 4
        self.story_middle_frame = tk.Frame(self.right_frame)
        self.story_middle_frame.pack(side="top", fill="x", expand=True)

        # Graph 3: scatter plot
        story_scatter = GraphManage.story_scatter(self.df)
        canvas = FigureCanvasTkAgg(story_scatter, master=self.story_middle_frame)
        canvas_widget_heatmap = canvas.get_tk_widget()
        canvas_widget_heatmap.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # Graph 4: correlation heat map
        story_heatmap = GraphManage.story_heatmap(self.df)
        canvas = FigureCanvasTkAgg(story_heatmap, master=self.story_middle_frame)
        canvas_widget_heatmap = canvas.get_tk_widget()
        canvas_widget_heatmap.pack(side="left", fill="both", expand=True)
        canvas.draw()

        # Bottom sub frame for label 2
        story_bottom_frame = tk.Frame(self.right_frame)
        story_bottom_frame.pack(side="top", fill="x", expand=False)

        # Label 2: summary of the storytelling
        summary = ttk.Label(story_bottom_frame,
                            text='Our data highlights a trend: larger dogs often have shorter lifespans.\n'
                                 'Please consider this when selecting your new puppy.',
                            style='Small.TLabel')
        summary.pack(side="top", fill="both", expand=True)

    def story_combobox_handler(self, event):
        """ Handle combobox selection. """
        selected_var = self.selected_story_hist.get()
        if selected_var != self.default_story_combo:
            self.update_hist(selected_var)

    def update_hist(self, selected_var):
        """
        Update the histogram in the storytelling section
        by retrieving data from a combo box
        """
        self.canvas_widget.destroy()
        self.story_hist = GraphManage.create_histogram(self.df, selected_var)
        canvas = FigureCanvasTkAgg(self.story_hist, master=self.story_top_right_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.config(width=240, height=210)
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=(20, 70))

    # Page 3
    # def run_find_breeds_page3(self):
    #     self.clear_right_frame()
    #     self.page_find_breeds = 3
    #     self.progress_bar = ttk.Progressbar(self.right_frame, length=400, mode="indeterminate")
    #     self.progress_bar.pack(side="bottom")
    #     self.thread = Thread(target=self.find_breeds_page3)
    #     self.thread.start()
    #     self.progress_bar.start(10)
    #     self.after(10, self.check_ui)
    #
    # def check_ui(self):
    #     if self.thread.is_alive():
    #         self.after(10, self.check_ui)
    #     else:
    #         self.progress_bar.stop()

    def find_breeds_page3(self):
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
        combo_size = ttk.Combobox(right_frame, textvariable=self.selected_size, values=size_list,
                                  width=10, state='readonly', style='Custom.TCombobox')
        combo_size.pack(side="top", anchor='ne', padx=20, pady=(20, 25))
        combo_size.set('Select')

    # Page 4
    def find_breeds_page4(self, name_list, score_list):
        self.clear_right_frame()
        self.page_find_breeds = 4

        # Create frames for left and right columns
        left_frame = ttk.Frame(self.right_frame, style='TFrame')
        right_frame = ttk.Frame(self.right_frame, style='TFrame')
        left_frame.pack(side="left", fill="y", expand=True, padx=10, pady=10)
        right_frame.pack(side="right", fill="y", expand=True, padx=10, pady=10)

        score_graph = GraphManage.score_bar(name_list, score_list)
        canvas = FigureCanvasTkAgg(score_graph, master=left_frame)
        canvas_widget_score = canvas.get_tk_widget()
        canvas_widget_score.pack(side="left", expand=True)
        canvas.draw()

        # best_match = ttk.Label(left_frame, text=f'Your Best Match\n\n'
        #                                         f': {name_list[0]}\n\n\n\n\n\n\n'
        #                                         f'Click "Next" to see\n\n'
        #                                         f'more information\n\n'
        #                                         f'about your best match !',
        #                        style='TLabel')

        best_match = ttk.Label(right_frame, text=f'Your Best Match\n\n'
                                                 f': {name_list[0]}\n\n\n\n\n\n\n'
                                                 f'Select breed\n\n'
                                                 f'to see more information')
        best_match.pack(padx=10, expand=True)

        self.combobox_breed1 = ttk.Combobox(right_frame, textvariable=self.selected_breed_combo,
                                            values=name_list, state='readonly', style='Custom.TCombobox')
        self.combobox_breed1.pack(anchor='n', padx=10, expand=True)
        self.combobox_breed1.set('Select')

    def get_user_prefer(self):
        prefer_list = [self.entry_adapt.get(), self.entry_friendly.get(), self.entry_health.get(),
                       self.entry_train.get(), self.entry_exercise.get(), self.entry_life.get(),
                       self.selected_size.get()]
        return prefer_list

    # Statistical Information
    def dog_info_page(self):
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

        left_frame = ttk.Frame(self.right_frame, style='TFrame')
        right_frame = ttk.Frame(self.right_frame, style='TFrame')
        left_frame.pack(side='left', fill='y', expand=True, padx=10, pady=10)
        right_frame.pack(side='right', fill='y', expand=True, padx=10, pady=10)

        breed_label = ttk.Label(left_frame, text=breed, style='WhiteCenter.TLabel')
        breed_label.pack(side='top', expand=True)

        info_label = ttk.Label(right_frame, text=f'Breed Group: {breed_group}         Size: {breed_size}\n\n'
                                                 f'Minimum Lifespan: {min_lifespan}      Max Lifespan: {max_lifespan}',
                               style='TLabel')
        info_label.pack(expand=True, pady=10)

        char_bar = GraphManage.create_char_bar(self.df, breed)
        canvas = FigureCanvasTkAgg(char_bar, master=right_frame)
        canvas_widget_score = canvas.get_tk_widget()
        canvas_widget_score.pack(side='top', anchor='n', expand=True)
        canvas.draw()

    def statistical_page1(self):
        # Clear some elements
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

        # Configure grid for expansion and alignment
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, minsize=50)
        self.right_frame.grid_rowconfigure(1, minsize=50)
        self.right_frame.grid_rowconfigure(2, minsize=50)
        self.right_frame.grid_rowconfigure(3, minsize=100)
        self.right_frame.grid_rowconfigure(4, minsize=70)

        # # Label and entry for entering breed
        # self.label_enter_breed = ttk.Label(self.right_frame, text='Enter dog breed', style='TLabel')
        # self.label_enter_breed.grid(row=0, column=0, padx=90, pady=(30, 0), sticky='ew')
        # self.entry_breed = ttk.Entry(self.right_frame, style='TEntry')
        # self.entry_breed.grid(row=1, column=0, padx=90, pady=(10, 0), sticky='ew')
        # self.entry_breed.focus()

        # Label and combobox for choosing a breed
        self.label_choose_breed = ttk.Label(self.right_frame, text='Choose dog breed', style='TLabel')
        self.label_choose_breed.grid(row=0, column=0, padx=170, pady=(70, 0), sticky='ew')
        self.combobox_breed2 = ttk.Combobox(self.right_frame, width=30, textvariable=self.selected_breed_combo,
                                            values=sorted_breed_list, state='readonly', style='Custom.TCombobox')
        self.combobox_breed2.grid(row=1, column=0, padx=170, pady=(20, 0), sticky='ew')
        self.combobox_breed2.set('Select')

        # Button to show information
        self.show_info_button = ttk.Button(self.right_frame, text='Show Information', style='TButton',
                                           command=self.controller.show_info_handler)
        self.show_info_button.grid(row=2, column=0, padx=170, pady=20, sticky='ew')

        # Label for data exploration section
        self.explore_label = ttk.Label(self.right_frame,
                                       text='Data exploration\n\n'
                                            'Select attributes and plot your own graph',
                                       style='TLabel')
        self.explore_label.grid(row=3, column=0, padx=170, pady=0, sticky='ew')

        # Button for exploring data
        self.explore_button = ttk.Button(self.right_frame, text='Explore', style='TButton')
        self.explore_button.grid(row=4, column=0, padx=170, pady=0, sticky='new')

    def comparison_page1(self):
        self.menu_label.destroy()
        try:
            self.next_button.destroy()
        except AttributeError:
            pass
        self.clear_right_frame()
        self.menu_label = ttk.Label(self.top_frame, text="Characteristics Comparison",
                                    style='TLabel', padding=(45, 0))
        self.menu_label.pack()

    # def user_preference(self, command):
    #     if command == 'find':
    #         pass
    #     elif command == 'show_breed':
    #         if self.entry_breed.get():
    #             return self.entry_breed.get()
    #         else:
    #             return self.selected_breed.get()
    #     elif command == 'select_1breed':
    #         pass
    #     elif command == 'select_2breed':
    #         pass

    def inform_error(self, inform_text):
        try:
            self.inform.destroy()
        except AttributeError:
            pass
        self.inform = ttk.Label(self.bottom_frame, text=inform_text,
                                background='#FFFAF0', foreground='red',
                                font=('Times New Roman', 20))
        self.inform.pack(side='left', anchor='e', expand=True)
        self.after(2000, self.inform.destroy)

    def run(self):
        """
        Run the program (CalculatorView)
        :return:
        """
        self.mainloop()
