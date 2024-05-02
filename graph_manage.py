import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphManage:
    def __init__(self):
        pass

    @staticmethod
    def load_data(filepath):
        """
        Load and preprocess data from a CSV file.
        """
        df = pd.read_csv(filepath)
        df['average_lifespan'] = (df['min_life_expectancy'] + df['max_life_expectancy']) / 2

        df['average_size'] = (df['max_height_male'] + df['max_weight_male'] + df['min_height_male'] +
                              df['min_weight_male'] + df['max_height_female'] + df['max_weight_female'] +
                              df['min_height_female'] + df['min_weight_female']) / 8

        bins = [0, 17.3125, 47.46875, 100.25]
        size_labels = ['small', 'medium', 'big']
        df['size_category'] = pd.cut(df['average_size'], bins=bins, labels=size_labels, include_lowest=True)

        return df

    @staticmethod
    def create_histogram(df, selected_var):
        """
        Creates a histogram figure of the specified variable from the dataframe.
        """
        if selected_var in df.columns:
            fig = Figure(figsize=(3, 3))
            ax = fig.add_subplot(111)
            df.hist(column=selected_var, ax=ax)
            ax.set_title(f'{selected_var} Histogram', fontsize=6)
            ax.set_xlabel(selected_var, fontsize=6)
            ax.set_ylabel('Frequency', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=6)

            fig.tight_layout(pad=1.0)

            return fig

    def story_scatter(self):
        pass

    def story_corr_heat(self):
        pass

    @staticmethod
    def story_bar(df):
        if 'size_category' in df.columns:
            df['size_category'] = pd.Categorical(df['size_category'], categories=['small', 'medium', 'big'], ordered=True)

            fig = Figure(figsize=(2, 2))
            ax = fig.add_subplot(111)

            bar_plot = sns.barplot(x='size_category', y='average_lifespan', data=df, order=['small', 'medium', 'big'], ax=ax)

            colors = ['#27408B', '#008080', '#71C671']
            for i, bar in enumerate(bar_plot.patches):
                bar.set_color(colors[i % len(colors)])

            ax.set_title('Average Lifespan by Size Category', fontsize=6)
            ax.set_xlabel('Size Category', fontsize=6)
            ax.set_ylabel('Average Lifespan (Years)', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=6)

            fig.tight_layout(pad=0.5)

            return fig
