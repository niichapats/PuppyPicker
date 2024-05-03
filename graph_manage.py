import pandas as pd
import seaborn as sns
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
    def create_bar(df, title, x_axis, y_axis, x_label, y_label, color):
        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        ax.barplot(x=x_axis, y=y_axis, data=df, ax=ax, color=color)

        ax.set_title(title, fontsize=6)
        ax.set_xlabel(x_label, fontsize=6)
        ax.set_ylabel(y_label, fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        fig.tight_layout(pad=0.5)

        return fig

    @staticmethod
    def score_bar(x_axis, y_axis):
        fig = Figure(figsize=(4, 4.5))
        ax = fig.add_subplot(111)

        ax.bar(x_axis, y_axis, color='#E9967A')

        ax.set_title('Scores of the top 5 dogs that\n'
                     'best match your preferences', fontsize=11)
        ax.set_xlabel('Breeds', fontsize=9)
        ax.set_ylabel('Score', fontsize=9)
        ax.tick_params(axis='both', which='major', labelsize=8)

        ax.set_xticks(range(len(x_axis)))
        ax.set_xticklabels(x_axis, rotation=45)

        fig.tight_layout(pad=0.75)

        return fig
