from dash import html, dcc, dash_table
import dash_mantine_components as dmc
# import dash_bootstrap_components as dbc

data = [["csv", "csv"], ["xsls", "xsls"], [
    "pdf", "pdf"], ["html", "html"], ["xml", "xml"]]

layout = html.Div([  # This is the main layout of the app

    # Sidebar
    html.Div([
        dmc.Button("Button 1", id="btn-1",
                   style={"display": "block", "marginBottom": "10px"}),
        dmc.Button("Button 2", id="btn-2",
                   style={"display": "block", "marginBottom": "10px"}),
        dmc.Button("Button 3", id="btn-3",
                   style={"display": "block", "marginBottom": "10px"}),
        # Add more buttons or other components here as needed
    ], style={'border': '1px solid black', 'width': '20%', 'height': '90vh', 'margin': '1rem auto 0 auto', 'padding': '1rem', 'borderRadius': '10px'}),


    html.Div([
        html.Div([
            dcc.Upload(  # This is the upload button
                id='upload-data',
                children=dmc.Button("Upload File",
                                    style={"backgroundColor": "#0C7FDA"}),
                multiple=True
            ),
            html.Div([  # This is the dropdown and download button
                dmc.Select(
                    id="framework-select",
                    data=[
                        {"value": "csv", "label": "csv"},
                        {"value": "xsls", "label": "xsls"},
                        {"value": "html", "label": "html"},
                        {"value": "xml", "label": "xml"},
                        {"value": "pdf", "label": "pdf"},
                    ],
                ),
                dmc.Button("Export",
                           id="btn-download",
                           style={"backgroundColor": "#0C7FDA"}
                           ),
                dcc.Download(id="download-file")
            ], style={"display": "flex", "justifyContent": "flex-end", "alignItems": "center", "gap": "1rem"}
            ),
        ], style={'margin': '1rem auto 0 auto', 'width': '100%', "display": "flex", "justifyContent": "space-between", "alignItems": "center"}
        ),

        dcc.Loading(
            id="loading-table",
            type="default",
            fullscreen=False,
            children=dash_table.DataTable(  # This is the table that will display the data
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
                style_table={'overflowX': 'auto', 'overflowY': 'auto',
                             'height': '80vh', 'max-width': '100%'},
                style_cell={'textAlign': 'left'},
                # fixed_rows={'headers':True, 'data':1}  # Fix header rows at the top
            )
        )], style={'border': '1px solid black', 'width': '80%', 'height': '90vh', 'margin': '1rem auto 0 auto', 'padding': '1rem'})
], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
