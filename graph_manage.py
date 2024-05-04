import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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
            fig = Figure(figsize=(4, 3))
            ax = fig.add_subplot(111)
            df.hist(column=selected_var, ax=ax, color='#CDC673')
            ax.set_title(f'{selected_var} Histogram', fontsize=6)
            ax.set_xlabel(selected_var, fontsize=6)
            ax.set_ylabel('Frequency', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=6)

            fig.tight_layout(pad=2.5)

            return fig

    @staticmethod
    def story_scatter(df):
        if 'average_lifespan' in df.columns and 'average_size' in df.columns:
            fig = Figure(figsize=(2.5, 2))
            ax = fig.subplots()

            sns.scatterplot(data=df, x='average_size', y='average_lifespan', ax=ax, color='#9370DB')

            ax.set_title('Size vs. Lifespan Scatter plot', fontsize=6)
            ax.set_xlabel('Average Size (Height and Weight Combined)', fontsize=6)
            ax.set_ylabel('Average Lifespan (Years)', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=6)
            ax.grid(True)
            fig.tight_layout(pad=0.5)

            return fig

    @staticmethod
    def story_heatmap(df):
        if 'average_lifespan' in df.columns and 'average_size' in df.columns:
            fig = Figure(figsize=(2.5, 2))
            ax = fig.subplots()

            selected_columns = df[['average_lifespan', 'average_size']]
            correlation_matrix = selected_columns.corr()

            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f",
                        linewidths=.5, cbar_kws={"shrink": .8}, ax=ax)

            ax.set_title('Correlation Heatmap', fontsize=6)
            ax.tick_params(axis='both', which='major', labelsize=6)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            fig.tight_layout(pad=0.5)

            return fig

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

    @staticmethod
    def create_char_bar(df, breed):

        selected_breeds = [breed]
        characteristics = ['all_around_friendliness', 'trainability', 'health_grooming', 'exercise_needs', 'adaptability']

        selected_data = df[df['breed'].isin(selected_breeds)][['breed'] + characteristics]

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

            # Adjust layout
            fig.tight_layout(pad=0.5)

        return fig

    @staticmethod
    def score_bar(x_axis, y_axis):
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

    @staticmethod
    def gender_bar(gender, y_axis):
        x_axis = ['Min height', 'Max Height', 'Min Weight', 'Max Weight']
        fig = Figure(figsize=(3, 3))
        ax = fig.add_subplot(111)

        if gender == 'Male':
            bar_plot = ax.bar(x_axis, y_axis)
            colors = ['#AFA3D1', '#8E7FCD', '#89A5D4', '#596EAD']
            for i, bar in enumerate(bar_plot.patches):
                bar.set_color(colors[i % len(colors)])
        elif gender == 'Female':
            bar_plot = ax.bar(x_axis, y_axis)
            colors = ['#D1A3D1', '#CD7FC1', '#D89C9C', '#CB7988']
            for i, bar in enumerate(bar_plot.patches):
                bar.set_color(colors[i % len(colors)])

        ax.set_xlabel('Breeds', fontsize=9)
        ax.set_ylabel('Score', fontsize=9)
        ax.tick_params(axis='both', which='major', labelsize=8)

        ax.set_xticks(range(len(x_axis)))
        ax.set_xticklabels(x_axis, rotation=45)

        fig.tight_layout(pad=0.5)

        return fig

