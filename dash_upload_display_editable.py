from dash import Dash, dcc, html, dash_table, Input, Output, State, callback, dash_table

import base64
import datetime
import io

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload File'),
         # Allow multiple files to be uploaded
        multiple=True),
        
    dash_table.DataTable(
        id='editable-table',  # Assign an ID to the DataTable component
        editable=True,  # Enable editing
        style_table={'height': '70vh', 'overflowX': 'auto'},  # Add horizontal scroll if needed
    ),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


@app.callback(
    Output('editable-table', 'data'),
    Output('editable-table', 'columns'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is None:
        return [], []  # Return empty data and columns if no contents are uploaded

    df = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])

    # Create columns for the DataTable
    columns = [{'name': col, 'id': col} for col in df.columns]

    return df.to_dict('records'), columns

if __name__ == '__main__':
    app.run(debug=True)
