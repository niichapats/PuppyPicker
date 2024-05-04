"""  Model for Puppy Picker"""
from graph_manage import GraphManage


class PuppyPickerModel:
    def __init__(self):
        self.df = GraphManage.load_data('breeds.csv')

    def find_matching_breeds(self, preference: list):
        columns = ['adaptability', 'all_around_friendliness', 'health_grooming',
                   'trainability', 'exercise_needs', 'average_lifespan']
        if preference[6] == 'all':
            df_temp = self.df.copy()
        else:
            df_temp = self.df[self.df['size_category'] == preference[6]].copy()

        for index in range(6):
            df_temp['score_' + columns[index]] = df_temp[columns[index]] * int(preference[index])

        df_temp['sum_score'] = df_temp['adaptability'] + df_temp['all_around_friendliness'] \
                               + df_temp['health_grooming'] + df_temp['trainability'] \
                               + df_temp['exercise_needs'] + df_temp['average_lifespan']

        top_rows = df_temp.sort_values(by='sum_score', ascending=False).head(5)
        top_name = top_rows['breed'].tolist()
        top_score = top_rows['sum_score'].tolist()
        return top_name, top_score

    def descriptive_lifespan(self):
        min_lifespan = self.df['average_lifespan'].min()
        max_lifespan = self.df['average_lifespan'].max()
        average_lifespan = self.df['average_lifespan'].mean()
        mode_lifespan = self.df['average_lifespan'].mode()

        if not mode_lifespan.empty:
            mode_lifespan = mode_lifespan.iloc[0]

        list_data = [int(min_lifespan), int(max_lifespan), int(average_lifespan), int(mode_lifespan)]
        return list_data
