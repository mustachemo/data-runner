from dash import html, dcc, dash_table
import dash_mantine_components as dmc
# import dash_bootstrap_components as dbc

data = [["csv", "csv"], ["xsls", "xsls"], [
    "pdf", "pdf"], ["html", "html"], ["xml", "xml"]]

layout = html.Div([  # This is the main layout of the app
    # This will hold the data uploaded by the user in memory
    dcc.Store(id='df-store'),
    dcc.Download(id="download-file"),

    html.Div([
        dcc.Upload(  # This is the upload button
            id='upload-data',
            # This is the button that will be displayed
            children=html.Button('Import'),
            style={"display": "inline-block"},
            multiple=True  # Allow multiple files to be uploaded
        ),
        html.Div([
            dmc.Button("Export", id="btn-download",
                       style={"backgroundColor": "#0C7FDA"}),
            dmc.Select(
                # placeholder="Select one",
                id="framework-select",
                data=[
                    {"value": "csv", "label": "csv"},
                    {"value": "xsls", "label": "xsls"},
                    {"value": "html", "label": "html"},
                    {"value": "xml", "label": "xml"},
                    {"value": "pdf", "label": "pdf"},
                ],
            ),
        ], style={"display": "flex", "justifyContent": "flex-end", "alignItems": "center", "gap": "1rem", "border": "1px solid black"}
        ),

    ], style={'margin': '1rem auto 0 auto', 'width': '90%', "display": "flex", "justifyContent": "flex-end", "alignItems": "center", "gap": "1rem", "border": "1px solid black"}
    ),


    dash_table.DataTable(  # This is the table that will display the data
        id='editable-table',  # Assign an ID to the DataTable component
        editable=True,  # Enable editing,
        column_selectable="multi",  # This enables column selection
        row_selectable='multi',  # This enables row selection
        # This enables virtualization, which allows large data sets to be rendered efficiently
        virtualization=True,
        # selected_columns=[],
        # selected_rowss=[],
        sort_action='native',  # This enables data to be sorted by the user
        filter_action='native',  # This enables data to be filtered by the user
        row_deletable=True,  # This enables users to delete rows
        style_table={'height': '70vh', 'width': '90%',
                     'overflowX': 'auto', 'margin': '1rem auto 0 auto'},
        # left align text in columns for readability
        style_cell={'textAlign': 'left'},
        # fixed_rows={'headers':True, 'data':1}  # Fix header rows at the top
    ),
])
