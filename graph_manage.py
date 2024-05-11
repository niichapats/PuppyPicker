"""
Module for managing data visualization in the Puppy Picker
"""

import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.figure import Figure


class GraphManage:
    """
    Manages data loading, processing, and visualization
    for the Puppy Picker.
    """
    def __init__(self):
        self.df = self.load_data('breeds.csv')

    @staticmethod
    def load_data(filepath):
        """
        Load and preprocess data from a CSV file, enhancing the dataset
        with calculated fields like average lifespan and size category for detailed analysis.
        """
        df = pd.read_csv(filepath)
        df['average_lifespan'] = (df['min_life_expectancy'] + df['max_life_expectancy']) / 2

        df['average_size'] = (df['max_height_male'] + df['max_weight_male'] + df['min_height_male'] +
                              df['min_weight_male'] + df['max_height_female'] + df['max_weight_female'] +
                              df['min_height_female'] + df['min_weight_female']) / 8

        bins = [0, 17.3125, 47.46875, 100.25]
        size_labels = ['small', 'medium', 'big']
        df['size_category'] = pd.cut(df['average_size'], bins=bins, labels=size_labels,
                                     include_lowest=True)
        return df

    def create_histogram(self, selected_var, size):
        """
        Creates a histogram figure of the specified variable
        from the dataframe based on the specified size of the graph.
        """
        if size == 'small':
            fig = Figure(figsize=(4, 3))
            ax = fig.add_subplot(111)
            self.df.hist(column=selected_var, ax=ax, color='#CDC673')
            ax.set_title(f'{selected_var} Histogram', fontsize=6)
            ax.set_xlabel(selected_var, fontsize=6)
            ax.set_ylabel('Frequency', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=6)
            fig.tight_layout(pad=2.5)
            return fig
        elif size == 'big':
            fig = Figure(figsize=(5.5, 3.5))
            ax = fig.add_subplot(111)
            self.df.hist(column=selected_var, ax=ax, color='#CDC673')
            ax.set_title(f'{selected_var} Histogram', fontsize=8)
            ax.set_xlabel(selected_var, fontsize=8)
            ax.set_ylabel('Frequency', fontsize=8)
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.tick_params(axis='x', labelrotation=45)
            fig.tight_layout()
            return fig

    def story_scatter(self):
        """
        Creates a scatter plot comparing average size and lifespan across
        dog breeds in the dataset. This plot is used on the storytelling page
        """
        fig = Figure(figsize=(2.5, 2))
        ax = fig.add_subplot(111)

        sns.scatterplot(data=self.df, x='average_size',
                        y='average_lifespan', ax=ax, color='#9370DB')

        ax.set_title('Size vs. Lifespan Scatter plot', fontsize=6)
        ax.set_xlabel('Average Size (Height and Weight Combined)', fontsize=6)
        ax.set_ylabel('Average Lifespan (Years)', fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        ax.grid(True)
        fig.tight_layout(pad=0.5)

        return fig

    def story_heatmap(self):
        """
        Creates a heatmap showing correlations between average size and
        lifespan within the breed dataset. This plot is used on the storytelling page
        """
        fig = Figure(figsize=(2.5, 2))
        ax = fig.add_subplot(111)

        selected_columns = self.df[['average_lifespan', 'average_size']]
        correlation_matrix = selected_columns.corr()

        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f",
                    linewidths=.5, cbar_kws={"shrink": .8}, ax=ax)

        ax.set_title('Correlation Heatmap', fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        fig.tight_layout(pad=0.5)

        return fig

    def story_bar(self):
        """
        Creates a bar graph showing the average lifespan of dog breeds
        categorized by size. This plot is used on the storytelling page
        """
        self.df['size_category'] = pd.Categorical(self.df['size_category'],
                                                  categories=['small', 'medium', 'big'],
                                                  ordered=True)

        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        bar_plot = sns.barplot(x='size_category', y='average_lifespan', data=self.df,
                               order=['small', 'medium', 'big'], ax=ax)

        colors = ['#27408B', '#008080', '#71C671']
        for i, each_bar in enumerate(bar_plot.patches):
            each_bar.set_color(colors[i % len(colors)])
        ax.set_title('Average Lifespan by Size Category', fontsize=6)
        ax.set_xlabel('Size Category', fontsize=6)
        ax.set_ylabel('Average Lifespan (Years)', fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        fig.tight_layout(pad=0.5)

        return fig

    def char_bar(self, breed):
        """
        Creates a bar graph displaying scores of various characteristics
        for a specific dog breed. This plot is used on the Statistical Information page
        """

        selected_breeds = [breed]
        characteristics = ['all_around_friendliness', 'trainability',
                           'health_grooming', 'exercise_needs', 'adaptability']

        selected_data = self.df[self.df['breed'].isin(selected_breeds)][['breed'] + characteristics]

        fig = Figure(figsize=(3.5, 3.5))
        ax = fig.add_subplot(111)

        if not selected_data.empty:
            data_for_plotting = selected_data[characteristics].iloc[0].values
            index = np.arange(len(characteristics))

            ax.bar(index, data_for_plotting, color='#66CDAA')

            ax.set_title('Characteristic score', fontsize=11)
            ax.set_xlabel('Characteristics', fontsize=9)
            ax.set_ylabel('Scores (0-5)', fontsize=9)
            ax.set_xticks(index)
            ax.set_xticklabels(characteristics, rotation=45, ha="right")
            ax.tick_params(axis='both', which='major', labelsize=8)

            fig.tight_layout(pad=0.5)

        return fig

    @staticmethod
    def score_bar(x_axis, y_axis):
        """
        Creates a bar graph displaying scores of
        various characteristics for a specific dog breed.
        """
        fig = Figure(figsize=(3.5, 4))
        ax = fig.add_subplot(111)

        ax.bar(x_axis, y_axis, color='#E9967A')

        ax.set_title('Scores of the top 5 dogs that\n'
                     'best match your preferences', fontsize=10)
        ax.set_xlabel('Breeds', fontsize=8)
        ax.set_ylabel('Score', fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)

        ax.set_xticks(range(len(x_axis)))
        ax.set_xticklabels(x_axis, rotation=45)

        fig.tight_layout(pad=0.5)

        return fig

    def male_bar(self, breed):
        """
        Creates a bar graph illustrating physical measurements
        for male dogs of a selected breed.
        """
        x_axis = ['Min height', 'Max Height', 'Min Weight', 'Max Weight']
        min_height_m = self.df[self.df['breed'] == breed]['min_height_male'].iloc[0]
        max_height_m = self.df[self.df['breed'] == breed]['max_height_male'].iloc[0]
        min_weight_m = self.df[self.df['breed'] == breed]['min_weight_male'].iloc[0]
        max_weight_m = self.df[self.df['breed'] == breed]['max_weight_male'].iloc[0]
        y_axis = [min_height_m, max_height_m, min_weight_m, max_weight_m]

        fig = Figure(figsize=(3, 3.3))
        ax = fig.add_subplot(111)
        colors = ['#AFA3D1', '#8E7FCD', '#89A5D4', '#596EAD']

        ax.bar(x_axis, y_axis, color=colors)

        ax.set_xlabel('Measurements', fontsize=9)
        ax.set_ylabel('Inches (Height)\nPounds (Weight)', fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_xticks(range(len(x_axis)))
        ax.set_xticklabels(x_axis, rotation=45)

        fig.tight_layout(pad=0.5)

        return fig

    def female_bar(self, breed):
        """
        Creates a bar graph illustrating physical measurements
        for female dogs of a selected breed.
        """
        x_axis = ['Min height', 'Max Height', 'Min Weight', 'Max Weight']
        min_height_f = self.df[self.df['breed'] == breed]['min_height_female'].iloc[0]
        max_height_f = self.df[self.df['breed'] == breed]['max_height_female'].iloc[0]
        min_weight_f = self.df[self.df['breed'] == breed]['min_weight_female'].iloc[0]
        max_weight_f = self.df[self.df['breed'] == breed]['max_weight_female'].iloc[0]
        y_axis = [min_height_f, max_height_f, min_weight_f, max_weight_f]

        fig = Figure(figsize=(3, 3.3))
        ax = fig.add_subplot(111)
        colors = ['#D1A3D1', '#CD7FC1', '#D89C9C', '#CB7988']

        ax.bar(x_axis, y_axis, color=colors)

        ax.set_xlabel('Measurements', fontsize=9)
        ax.set_ylabel('Inches (Height)\nPounds (Weight)', fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_xticks(range(len(x_axis)))
        ax.set_xticklabels(x_axis, rotation=45)

        fig.tight_layout(pad=0.5)

        return fig

    def explore_bar(self, x_axis, y_axis):
        """
        Creates a bar graph based on user-selected attributes for exploratory data analysis.
        """
        fig = Figure(figsize=(5.5, 3.5))
        ax = fig.add_subplot(111)

        sns.barplot(data=self.df, x=x_axis, y=y_axis, ax=ax, color='#E88989')

        ax.set_title(f'{x_axis} vs. {y_axis}', fontsize=8)
        ax.set_xlabel(x_axis, fontsize=8)
        ax.set_ylabel(y_axis, fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.tick_params(axis='x', labelrotation=45)

        fig.tight_layout()

        return fig

    def explore_scatter(self, x_axis, y_axis):
        """
        Creates a scatter plot based on user-selected attributes for exploratory data analysis.
        """
        fig = Figure(figsize=(5.5, 3.5))
        ax = fig.add_subplot(111)

        sns.scatterplot(data=self.df, x=x_axis, y=y_axis, ax=ax, color='#E694C7')

        ax.set_title(f'{x_axis} vs. {y_axis}', fontsize=8)
        ax.set_xlabel(x_axis, fontsize=8)
        ax.set_ylabel(y_axis, fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.tick_params(axis='x', labelrotation=45)

        fig.tight_layout()

        return fig

    def explore_breed_group_histgram(self, selected_group, selected_attribute):
        """
        Creates a histogram for a selected breed group and attribute,
        aiding in detailed data exploration.
        """
        filtered_df = self.df[self.df['breed_group'] == selected_group]
        fig = Figure(figsize=(5.5, 3.5))
        ax = fig.add_subplot(111)
        filtered_df.hist(column=selected_attribute, ax=ax, color='#CDC673')
        ax.set_title(f'{selected_attribute} Histogram of {selected_group}', fontsize=10)
        ax.set_xlabel(selected_attribute, fontsize=8)
        ax.set_ylabel('Frequency', fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)

        fig.tight_layout()

        return fig

    def compare_bar(self, breed1, breed2, compare):
        """
        Creates a comparison bar graph showing characteristics
        of two selected dog breeds side by side.
        """
        breed1_data = [self.df.loc[self.df['breed'] == breed1, comp].iloc[0] for comp in compare]
        breed2_data = [self.df.loc[self.df['breed'] == breed2, comp].iloc[0] for comp in compare]

        fig = Figure(figsize=(5.5, 3.7))
        ax = fig.add_subplot(111)
        x_axis = np.arange(len(compare))
        ax.bar(x_axis - 0.2, breed1_data, 0.4, label=breed1, color='#D1E1A4')
        ax.bar(x_axis + 0.2, breed2_data, 0.4, label=breed2, color='#6DCDBC')

        ax.set_xlabel('Characteristics', fontsize=8)
        ax.set_ylabel('Scores', fontsize=8)
        ax.set_title('Comparison of Dog Breed Characteristics', fontsize=9.5)
        ax.legend(fontsize=8)
        ax.set_xticks(x_axis)
        ax.set_yticks([0, 1, 2, 3, 4, 5])
        ax.set_xticklabels(compare, rotation=45)
        ax.tick_params(axis='both', which='major', labelsize=8)
        fig.tight_layout(pad=1.5)

        return fig
