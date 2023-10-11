from dash import html
import pandas as pd


def get_data_analysis(data):

    df = pd.DataFrame.from_dict(data)

    empty_corrupt_values = df.isna().sum()
    num_duplicate_rows = df.duplicated().sum()

    if (empty_corrupt_values.sum() != 0):
        return [
            html.Li([
                "Data: ",
                html.Span(f'{"{:,}".format(df.size)}', style={
                    'color': '#007BFF',
                    'fontWeight': 'bold',
                    'padding': '0 5px',
                    'borderRadius': '5px'
                })
                # i want ot get rid of the bulletd points
            ], style={"listStyleType": "none"}),
            html.Li([
                "Empty/Corrupt Cells: ",
                html.Span(f'{"{:,}".format(empty_corrupt_values.sum())}', style={
                    'color': '#007BFF',
                    'fontWeight': 'bold',
                    'padding': '0 5px',
                    'borderRadius': '5px'
                })
            ], style={"listStyleType": "none"}),
            html.Li([
                "Duplicate Rows: ",
                html.Span(f'{"{:,}".format(num_duplicate_rows)}', style={
                    'color': '#007BFF',
                    'fontWeight': 'bold',
                    'padding': '0 5px',
                    'borderRadius': '5px'
                })
            ], style={"listStyleType": "none"})
        ]
