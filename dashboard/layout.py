from dash import html, dcc, dash_table
import dash_mantine_components as dmc
# import dash_bootstrap_components as dbc

layout = html.Div([  # This is the main layout of the app

    # Sidebar
    html.Div([
        html.Div([
            dmc.Image(
                src="./assets/images/logo.jpeg", alt="USCS", width=40),
            dmc.Title(f"United States Cold Storage", order=5,),
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", "gap": "1rem", "marginBottom": "1rem", "borderBottom": "1px solid #ccc", 'padding': "1rem"}),
        dmc.Button("Enforce datatypes", id="btn-enforce-dtypes",
                   style={"marginBottom": "10px"}),
        dmc.Modal(
            title="Select a column to enforce a datatype",
            id="enforce-dtypes-modal",
            zIndex=10000,
            children=[
                dmc.Space(h=20),
                html.Div(id='column-type-selector'),
                dmc.Space(h=20),
                dmc.Group(
                    [
                        dmc.Button("Submit", id="modal-submit-button"),
                        dmc.Button(
                            "Close",
                            color="red",
                            variant="outline",
                            id="modal-close-button",
                        ),
                    ],
                    position="right",
                ),
            ],
        ),

    ], className="sidebar"),


    # Main content
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
                    style={"width": "80px"},
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
            ], className="export-group"),
        ], className="import-export-group"),

        dcc.Loading(
            id="loading-table",
            type="cube",
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
                style_table={'minHeight': '75vh', 'height': '75vh', 'maxWidth': '100%',
                             'overflowY': 'auto', 'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                # style_header={
                #     'backgroundColor': 'rgb(30, 30, 30)',
                #     'color': 'white'
                # },
                # style_data={
                #     'backgroundColor': 'rgb(50, 50, 50)',
                #     'color': 'white'
                # },
                # fixed_rows={'headers':True, 'data':1}  # Fix header rows at the top
            ), parent_style={'maxWidth': '100%', 'maxHeight': '100%'}
        )

    ], className="main-content")

], className="app-container")
