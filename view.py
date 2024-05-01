""" UI for Puppy Picker """

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_manage import DataManage


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
        self.geometry('1100x700')
        self.selected_breed = tk.StringVar()
        self.breed_name = ['Golden retriever', 'Pug', 'Puddle', 'Pom']
        self.df = DataManage.load_data('breeds.csv')
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
        style.configure('White.TLabel', background='white', foreground=light_brown_text, font=('Times New Roman', 20), padding=(20, 20))
        style.configure('TButton', background=white_bg, foreground=light_brown_text, font=('Times New Roman', 15))
        style.configure('TEntry', fieldbackground='white', foreground=brown_text)
        style.configure('Big.TButton', padding=[20, 10], font=('Times New Roman', 20))
        style.configure('Custom.TCombobox', foreground=light_brown_text, background='white')

        self.configure(bg='snow1')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create top frame
        self.top_frame = ttk.Frame(self, style='TFrame')
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.menu_label = ttk.Label(self.top_frame, text='', style='TLabel', padding=(60, 0))

        # Load and display the image
        image = Image.open('logo.png')
        image = image.resize((650, 120), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = ttk.Label(self.top_frame, image=photo)
        image_label.image = photo
        image_label.pack()

        # Create left and right frame
        self.left_frame = self.create_left_frame()
        self.left_frame.grid(row=1, column=0, sticky='ns')
        self.left_frame.grid_propagate(False)
        self.create_nav_button()

        self.right_frame = self.create_right_frame()
        self.right_frame.grid(row=1, column=1, sticky='nsew')
        self.right_frame.grid_propagate(False)

    def create_left_frame(self):
        """
        Left Frame for Navigation Buttons
        """
        left_frame = ttk.Frame(self, width=400, padding=5, style='TFrame')
        return left_frame

    def create_right_frame(self):
        """
        Right frame for display each functions of the program
        """
        right_frame = ttk.Frame(self, padding=5, style='TFrame')
        home_info = ttk.Label(right_frame, text="Welcome !\n\nLet's explore breed traits through detailed graphs and find your ideal match \n\nwith personalized recommendations.", style='White.TLabel')
        home_info.grid(row=1, column=0, sticky='nsew', padx=10, pady=(60, 0))
        return right_frame

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

    # def display_find_breeds1(self):
    #     # self.clear_right_frame()
    #     # ttk.Label(self.right_frame, text='Find Matching Breeds', style='TLabel', padding=(60, 0)).grid(sticky='nsew')
    #     self.clear_right_frame()
    #     ttk.Label(self.right_frame, text='Find Matching Breeds', style='TLabel', padding=(60, 0)).grid(sticky='nsew')
    #     selected_var = 'average_lifespan'  # This could be dynamically set
    #     fig = DataManage.create_histogram(self.df, selected_var, (1, 1))
    #     canvas = FigureCanvasTkAgg(fig, master=self.right_frame)  # Embed the figure in the right_frame
    #     canvas.draw()
    #     canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Find Matching Breeds
    def find_breeds_page1(self):
        self.menu_label.destroy()
        self.clear_right_frame()
        self.menu_label = ttk.Label(self.top_frame, text='Find Matching Breeds', style='TLabel', padding=(60, 0))
        self.menu_label.pack()

        menu_info = ttk.Label(self.right_frame, text="Choose size of a dog you prefer and\n\nand rate the importance you place on each\n\ncharacteristic when considering getting a dog.", style='White.TLabel')
        menu_info.grid(row=1, column=0, sticky='nsew', padx=10, pady=(60, 0))

    def find_breeds_page2(self):
        pass

    # Statistical Information
    def statistical_page1(self):
        self.menu_label.destroy()
        self.clear_right_frame()
        self.menu_label = ttk.Label(self.top_frame, text='Statistical Information', style='TLabel', padding=(55, 0))
        self.menu_label.pack()

        self.label_enter_breed = ttk.Label(self.right_frame, text='Enter dog breed', width=30, style='TLabel')
        self.label_enter_breed.grid(row=1, column=0, padx=20, pady=(60, 0), sticky='ew')
        self.entry_breed = ttk.Entry(self.right_frame, style='TEntry')
        self.entry_breed.grid(row=2, column=0, padx=20, pady=(10, 20), sticky='ew')
        self.entry_breed.focus()

        self.label_choose_breed = ttk.Label(self.right_frame, text='Or choose dog breed', style='TLabel')
        self.label_choose_breed.grid(row=1, column=1, padx=20, pady=(50, 0), sticky='ew')
        self.combobox_breed = ttk.Combobox(self.right_frame, width=30, textvariable=self.selected_breed, values=self.breed_name, state='readonly', style='Custom.TCombobox')
        self.combobox_breed.grid(row=2, column=1, padx=20, pady=(10, 20), sticky='ew')

        self.show_info_button = ttk.Button(self.right_frame, text='Show Information', style='TButton', command=self.controller.show_info_handler)
        self.show_info_button.grid(row=3, column=0, padx=20, pady=(10, 20), sticky='ew')

    def comparison_page1(self):
        self.menu_label.destroy()
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
        fig = DataManage.create_histogram(self.df, selected_var)
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
