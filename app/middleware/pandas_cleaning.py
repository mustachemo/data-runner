import pandas as pd
import os
from dash import Dash, html

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
relative_path = "static/dirty-data"
target_directory_path = os.path.join(parent_directory, relative_path)

df = pd.read_csv(os.path.join(target_directory_path, 'food_coded.csv'))

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])



app = Dash(__name__)

app.layout = html.Div([
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run(debug=True)




def checkFileContents(file):
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    print(f'df.head(5): {df.head(5)}')
    print(f'df.shape: {df.shape}')
    print(f'df.size: {df.size}')
    print(f'df.ndim: {df.ndim}')
    print(f'df.columns: {df.columns}')
    print(f'df.info(): {df.info()}')
    print(f'df.describe(): {df.describe()}')