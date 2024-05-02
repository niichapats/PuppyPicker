""" UI for Puppy Picker """

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
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
        # self.geometry('1100x700')
        self.minsize(width=1050, height=700)
        self.breed_name = ['Golden retriever', 'Pug', 'Puddle', 'Pom']
        self.df = GraphManage.load_data('breeds.csv')
        self.page_find_breeds = 0
        self.story_hist = tk.StringVar()
        self.default_story_combo = 'Select Histogram'
        self.story_hist.set(self.default_story_combo)
        self.selected_breed = tk.StringVar()
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

        style.configure('TLabel', background=light_brown_bg, foreground=light_brown_text, font=('Times New Roman', 20))
        style.configure('Small.TLabel', background=light_brown_bg, foreground=light_brown_text, font=('Times New Roman', 14))
        style.configure('WhiteCenter.TLabel', anchor='center', background='white', foreground=light_brown_text,
                        font=('Times New Roman', 20),
                        padding=20)
        style.configure('Centered.TLabel', anchor='center', font=('Times New Roman', 20),
                        background='white', foreground='#9C661F', padding=20)

        style.configure('TButton', background=white_bg, foreground=light_brown_text, font=('Times New Roman', 15))
        style.configure('TEntry', fieldbackground='white', foreground=brown_text)
        style.configure('Big.TButton', padding=[20, 10], font=('Times New Roman', 20))
        style.configure('Custom.TCombobox', foreground=light_brown_text, background='white')

        self.configure(bg='snow1')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create top
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
        self.right_frame.grid(row=1, column=1, sticky='nsew')
        # self.right_frame.grid_columnconfigure(0, weight=1, minsize=50)  # Control size of descriptive stats column
        # self.right_frame.grid_columnconfigure(1, weight=1, minsize=100)

        # Create bottom frame
        self.bottom_frame = self.create_bottom_frame()
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')
        # self.next_button = ttk.Button(self.bottom_frame, text='', style='TButton')

    def create_left_frame(self):
        """
        Left Frame for Navigation Buttons
        """
        left_frame = ttk.Frame(self, width=400, padding=0, style='TFrame')
        return left_frame

    def create_right_frame(self):
        right_frame = ttk.Frame(self, padding=5, style='TFrame')

        # right_frame.grid_columnconfigure(0, weight=1)  # Allow the column to expand
        # right_frame.grid_rowconfigure(1, weight=1)  # Allow the row to expand

        home_info = ttk.Label(right_frame,
                              text="Welcome !\n\nLet's explore breed traits through detailed graphs and \n\nfind your ideal match with personalized recommendations.",
                              style='WhiteCenter.TLabel')
        home_info.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=20, pady=(50, 0))

        return right_frame

    def create_bottom_frame(self):
        """
        Bottom frame for exit button, next button, skip button
        """
        bottom_frame = ttk.Frame(self)
        quit_button = ttk.Button(bottom_frame, text="Quit", style='Big.TButton', cursor="heart", command=self.destroy)
        quit_button.pack(side=tk.LEFT, padx=35, pady=25)
        # next_button = ttk.Button(bottom_frame, text="Next", style='Big.TButton', cursor="heart",
        #                          command=lambda: self.controller.next_button_handler(self.page_find_breeds))
        # next_button.pack(side=tk.RIGHT, padx=10, pady=10)
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
        current_value = self.story_hist.get()
        if current_value == self.default_story_combo:
            self.story_hist.set("")

    # Find Matching Breeds
    def find_breeds_page1(self):
        self.page_find_breeds = 1
        self.menu_label.destroy()
        try:
            self.next_button.destroy()  # Ensuring next_button exists before trying to destroy it
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
        menu_info.grid(row=1, column=0, sticky='nsew', padx=20, pady=(50, 0))

        self.next_button = ttk.Button(self.bottom_frame, text="Next", style='Big.TButton', cursor="heart",
                                      command=lambda: self.controller.next_button_handler(self.page_find_breeds))
        self.next_button.pack(side=tk.RIGHT, padx=35, pady=25)

    # def find_breeds_page2(self, data):
    #     self.page_find_breeds = 2
    #     self.clear_right_frame()
    #
    #     self.right_frame.grid_rowconfigure(0, minsize=50)
    #
    #     descriptive_stat = ttk.Label(self.right_frame,
    #                                  text=f'Descriptive Statistic\n'
    #                                       f'-----------------------\n'
    #                                       f'Average Lifespan\n'
    #                                       f'Min: {data[0]}\n'
    #                                       f'Max: {data[1]}\n'
    #                                       f'Mean: {data[2]}\n'
    #                                       f'Mode: {data[3]}',
    #                                  style='Small.TLabel')
    #     descriptive_stat.grid(row=1, column=0, sticky='nw', padx=20)
    #
    #     fig_bar = GraphManage.story_bar(self.df)
    #     canvas = FigureCanvasTkAgg(fig_bar, master=self.right_frame)
    #     canvas_widget_bar = canvas.get_tk_widget()
    #     canvas_widget_bar.grid(row=1, column=1)
    #     canvas.draw()
    #
    #     story_hist_list = ['max_lifespan', 'max_height_male', 'max_height_female', 'max_weight_male', 'max_weight_female']
    #     story_combobox = ttk.Combobox(self.right_frame, textvariable=self.story_hist, values=story_hist_list, state="readonly")
    #     story_combobox.grid(row=0, column=3, padx=50, pady=(20, 0))
    #     story_combobox.bind('<<ComboboxSelected>>', self.clear_default_text)
    #     story_combobox.bind('<<ComboboxSelected>>',
    #                         GraphManage.create_histogram(self.df, self.right_frame, self.story_hist.get(), 100, 100, 1, 3))

    def find_breeds_page2(self, data):
        self.page_find_breeds = 2
        self.clear_right_frame()

        self.right_frame.grid_rowconfigure(0, minsize=50)
        # self.right_frame.grid_rowconfigure(1, minsize=300)

        descriptive_stat = ttk.Label(self.right_frame,
                                     text=f'Descriptive Statistic\n'
                                          f'-----------------------\n'
                                          f'Average Lifespan\n'
                                          f'Min: {data[0]}\n'
                                          f'Max: {data[1]}\n'
                                          f'Mean: {data[2]}\n'
                                          f'Mode: {data[3]}',
                                     style='Small.TLabel')
        descriptive_stat.grid(row=1, column=0, sticky='nw', padx=20, pady=10)

        # Bar graph represent size and lifespan
        fig_bar = GraphManage.story_bar(self.df)
        canvas = FigureCanvasTkAgg(fig_bar, master=self.right_frame)
        canvas_widget_bar = canvas.get_tk_widget()
        canvas_widget_bar.grid(row=1, column=1, padx=10, pady=10)
        canvas.draw()

        # Graph frame for histogram
        self.graph_frame = ttk.Frame(self.right_frame)
        self.graph_frame.grid(row=1, column=3, padx=(10, 0), sticky='new')

        # Combobox for selecting histogram
        story_hist_list = ['max_life_expectancy', 'max_height_male', 'max_height_female', 'max_weight_male', 'max_weight_female']
        story_combobox = ttk.Combobox(self.right_frame, textvariable=self.story_hist, values=story_hist_list, state="readonly")
        story_combobox.grid(row=0, column=3, padx=60)
        story_combobox.bind('<<ComboboxSelected>>', self.story_combobox_handler)

    def story_combobox_handler(self, event):
        """ Handle combobox selection. """
        selected_var = self.story_hist.get()
        if selected_var != self.default_story_combo:
            self.update_hist(selected_var)

    def update_hist(self, selected_var):
        # Clear previous widgets in the graph frame
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Generate the figure using the selected variable
        fig = GraphManage.create_histogram(self.df, selected_var)

        # Create the canvas and add it to the graph frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        # Explicitly set the size of the canvas widget
        canvas_widget.config(width=240, height=210)
        canvas_widget.pack(fill=tk.BOTH, expand=True)  # Adjust packing options if necessary

    # Statistical Information
    def statistical_page1(self):
        # Clear some elements
        self.menu_label.destroy()
        try:
            self.next_button.destroy()  # Ensuring next_button exists before trying to destroy it
        except AttributeError:
            pass
        self.clear_right_frame()

        self.menu_label = ttk.Label(self.top_frame, text='Statistical Information', style='TLabel', padding=(55, 0))
        self.menu_label.pack()

        # Configure grid for expansion and alignment
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_rowconfigure(3, weight=1)
        self.right_frame.grid_rowconfigure(4, weight=1)
        self.right_frame.grid_rowconfigure(5, weight=1)

        # Label and entry for entering breed
        self.label_enter_breed = ttk.Label(self.right_frame, text='Enter dog breed', style='TLabel')
        self.label_enter_breed.grid(row=0, column=0, padx=90, pady=(30, 0), sticky='ew')
        self.entry_breed = ttk.Entry(self.right_frame, style='TEntry')
        self.entry_breed.grid(row=1, column=0, padx=90, pady=(10, 0), sticky='ew')
        self.entry_breed.focus()

        # Label and combobox for choosing a breed
        self.label_choose_breed = ttk.Label(self.right_frame, text='Or choose dog breed', style='TLabel')
        self.label_choose_breed.grid(row=2, column=0, padx=90, pady=(10, 0), sticky='ew')
        self.combobox_breed = ttk.Combobox(self.right_frame, width=30, textvariable=self.selected_breed,
                                           values=self.breed_name, state='readonly', style='Custom.TCombobox')
        self.combobox_breed.grid(row=3, column=0, padx=90, pady=(5, 10), sticky='ew')

        # Button to show information
        self.show_info_button = ttk.Button(self.right_frame, text='Show Information', style='TButton',
                                           command=self.controller.show_info_handler)
        self.show_info_button.grid(row=4, column=0, padx=90, pady=(0, 10), sticky='ew')

        # Label for data exploration section
        self.explore_label = ttk.Label(self.right_frame,
                                       text="[Data exploration] Select attributes and plot your own graph",
                                       style='TLabel', padding=(80, 10))
        self.explore_label.grid(row=5, column=0, padx=10, pady=(0, 0), sticky='ew')

        # Button for exploring data
        self.explore_button = ttk.Button(self.right_frame, text='Explore', style='TButton')
        self.explore_button.grid(row=6, column=0, padx=90, pady=(10, 0), sticky='ew')

    def comparison_page1(self):
        self.menu_label.destroy()
        try:
            self.next_button.destroy()
        except AttributeError:
            pass
        self.clear_right_frame()
        self.menu_label = ttk.Label(self.top_frame, text="Characteristics Comparison", style='TLabel', padding=(45, 0))
        self.menu_label.pack()

    def user_preference(self, command):
        if command == 'find':
            pass
        elif command == 'show_breed':
            if self.entry_breed.get():
                return self.entry_breed.get()
            else:
                return self.selected_breed.get()
        elif command == 'select_1breed':
            pass
        elif command == 'select_2breed':
            pass

    def display_graph_test(self):
        self.menu_label.destroy()
        self.clear_right_frame()
        self.menu_label = ttk.Label(self.top_frame, text='Find Matching Breeds', style='TLabel', padding=(60, 0))
        self.menu_label.pack()

        selected_var = 'average_lifespan'
        fig = GraphManage.create_histogram(self.df, selected_var)
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.config(width=500, height=400)
        canvas_widget.grid(row=4, column=0)
        canvas.draw()

    def run(self):
        """
        Run the program (CalculatorView)
        :return:
        """
        self.mainloop()
