from dash import Dash, dcc, html, dash_table, Input, Output, State, callback, dash_table, callback_context
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd

df = pd.DataFrame() 

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Check the Columns you want to display", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            # nav=True,
            in_navbar=True,
            label="Columns Selection",
        ),
        dbc.NavItem(dbc.NavLink("Page 1", href="#"))
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
    ),

    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload File'),
        style={},
        multiple=True # Allow multiple files to be uploaded
    ),
        
    dash_table.DataTable(
        id='editable-table',  # Assign an ID to the DataTable component
        editable=True,  # Enable editing,
        column_selectable="multi",
        row_selectable='multi',
        # selected_columns=[],
        # selected_rowss=[],
        sort_action='native',
        filter_action='native',
        row_deletable=True,
        style_table={'height': '70vh', 'width': '90%', 'overflowX': 'auto', 'margin': '1rem auto 0 auto'},
        style_cell={'textAlign': 'left'}, # left align text in columns for readability
        # fixed_rows={'headers':True, 'data':1}  # Fix header rows at the top
    ),
    dcc.RadioItems(['csv', 'xsls','pdf', 'html', 'xml'],  id='radio-items'), 
    dcc.Download(id="download-text")
])

@callback(
    Output("download-text", "data"),
    Input('radio-items', 'value'),
    prevent_initial_call=True,
)
def download_specific_file(value):
    if value == 'csv':
        return dict(content=df.to_csv(index=False), filename="data.csv")
    if value == 'xml':
        return dict(content=df.to_xml(index=False), filename="data.xml")
    if value == 'html':
        return dict(content=df.to_html(index=False), filename="data.html")



@app.callback(
    Output('editable-table', 'style_data_conditional'),
    Input('editable-table', 'selected_columns')
    # Input('editable-table', 'selected_rows')
)
# def update_styles(selected_columns, selected_rows):
def update_styles(selected_columns):
    styles = []

    if selected_columns:
        styles.extend([{'if': {'column_id': col}, 'background_color': '#D2F3FF'} for col in selected_columns])

    # if selected_rows:
    #     styles.extend([{'if': {'row_index': row}, 'background_color': '#7FFF7F'} for row in selected_rows])

    return styles


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    global df

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
    columns = [{'name': col, 'id': col, "selectable": True} for col in df.columns]

    return df.to_dict('records'), columns

if __name__ == '__main__':
    app.run(debug=True)