import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from matplotlib.figure import Figure

# df = pd.read_csv('breeds.csv')
# df['average_lifespan'] = (df['min_life_expectancy'] + df['max_life_expectancy']) / 2
# df['average_size'] = (df['max_height_male'] + df['max_weight_male'] + df['min_height_male'] + df['min_weight_male'] + df['max_height_female'] + df['max_weight_female'] + df['min_height_female'] + df['min_weight_female']) / 8
#
# bins = [0, 17.3125, 47.46875, 100.25]
# size_labels = ['small', 'medium', 'big']
# df['size_category'] = pd.cut(df['average_size'], bins=bins, labels=size_labels, include_lowest=True)


class DataManage:
    def __init__(self):
        pass

    @staticmethod
    def load_data(filepath):
        """
        Load and preprocess data from a CSV file.

        Args:
        filepath (str): The path to the CSV file.

        Returns:
        pd.DataFrame: The preprocessed DataFrame.
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

        Args:
        dataframe (pd.DataFrame): The data to plot.
        selected_var (str): The column name of the variable to plot.

        Returns:
        matplotlib.figure.Figure: The figure object containing the histogram.
        """
        fig = Figure()
        ax = fig.add_subplot(111)
        df.hist(column=selected_var, ax=ax)
        ax.set_title(f'{selected_var} Histogram')
        ax.set_xlabel(selected_var)
        ax.set_ylabel('Frequency')
        return fig

    def story_scatter(self):
        pass

    def story_corr_heat(self):
        pass

    # @staticmethod
    # def story_bar(df):
    #     if 'size_category' in df.columns:
    #         df['size_category'] = pd.Categorical(df['size_category'], categories=['small', 'medium', 'big'], ordered=True)
    #
    #         # Create the plot
    #         plt.figure(figsize=(10, 6))
    #         bar_plot = sns.barplot(x='size_category', y='average_lifespan', data=df, order=['small', 'medium', 'big'])
    #
    #         # Manually setting colors
    #         colors = ['#27408B', '#008080', '#71C671']  # Define colors for each category
    #         for i, bar in enumerate(bar_plot.patches):
    #             bar.set_color(colors[i % len(colors)])  # Set color to each bar
    #
    #         plt.title('Average Lifespan by Size Category')
    #         plt.xlabel('Size Category')
    #         plt.ylabel('Average Lifespan (Years)')
    #         plt.xticks(rotation=45)  # Rotate labels for better readability
    #
    #         # Return the figure object containing the plot
    #         return plt.gcf()

    @staticmethod
    def story_bar(df):
        if 'size_category' in df.columns:
            df['size_category'] = pd.Categorical(df['size_category'], categories=['small', 'medium', 'big'], ordered=True)

            # Create a new figure
            fig = Figure(figsize=(2, 2))
            ax = fig.add_subplot(111)

            # Create the bar plot
            bar_plot = sns.barplot(x='size_category', y='average_lifespan', data=df, order=['small', 'medium', 'big'], ax=ax)

            # Manually setting colors
            colors = ['blue', 'green', 'red']  # Define colors for each category
            for i, bar in enumerate(bar_plot.patches):
                bar.set_color(colors[i % len(colors)])  # Set color to each bar

            ax.set_title('Average Lifespan by Size Category')
            ax.set_xlabel('Size Category')
            ax.set_ylabel('Average Lifespan (Years)')

            # Setting smaller font sizes
            ax.set_title('Average Lifespan by Size Category', fontsize=6)
            ax.set_xlabel('Size Category', fontsize=5)
            ax.set_ylabel('Average Lifespan (Years)', fontsize=5)
            ax.tick_params(axis='both', which='major', labelsize=5)

            fig.tight_layout(pad=0.5)

            return fig

