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


def higlight_empty_nan_null_cells(columns):
    higlight_cells = [
        {
            'if': {
                'filter_query': '{{{}}} is blank'.format(col),
                'column_id': col
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        } for col in [col_dict['id'] for col_dict in columns]
    ]

    return higlight_cells


def generate_dtype_highlighting(columns):
    dtype_higlighting = []

    for col in columns:
        col_id = col['id']
        col_type = col.get('type', None)

        # if col_type == "text":
        #     dtype_higlighting.append({
        #         'if': {
        #             'column_id': col_id
        #         },
        #         'backgroundColor': 'lightblue'
        #     })

        if col_type == "numeric":
            dtype_higlighting.append({
                'if': {
                    'column_id': col_id
                },
                'backgroundColor': 'lightgreen'
            })

        elif col_type == "datetime":
            dtype_higlighting.append({
                'if': {
                    'column_id': col_id
                },
                'backgroundColor': 'lightyellow'
            })

    return dtype_higlighting
