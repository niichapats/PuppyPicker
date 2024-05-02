"""  Model for Puppy Picker"""
from graph_manage import GraphManage


class PuppyPickerModel:
    def __init__(self):
        self.df = GraphManage.load_data('breeds.csv')

    def find_matching_breeds(self, preference: list):
        pass

    def descriptive_lifespan(self):
        min_lifespan = self.df['average_lifespan'].min()
        max_lifespan = self.df['average_lifespan'].max()
        average_lifespan = self.df['average_lifespan'].mean()
        mode_lifespan = self.df['average_lifespan'].mode()

        if not mode_lifespan.empty:
            mode_lifespan = mode_lifespan.iloc[0]

        list_data = [int(min_lifespan), int(max_lifespan), int(average_lifespan), int(mode_lifespan)]
        return list_data
