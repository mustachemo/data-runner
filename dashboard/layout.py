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

  
        #Here should be the preferences subtitle
        #dmc.Button("Preferences", variant="subtle", style={ "marginBottom": "1px dashed black"}),
        dmc.Button("Preferences", variant="subtle", style={"borderBottom": "1px dashed black", "paddingBottom": "5px"}),


        dmc.Tooltip(
            multiline=True,
            width=220,
            withArrow=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            # transitionTimingFunction="ease",
            label="Enforce formatting for cells in the table. This will inform the cleaning function of specific formatting for selected columns. The cleaning function will be able to pick up on these formats and clean the data accordingly.",
            children=dmc.Button("Enforce Formatting", id="btn-enforce-format",
                                style={"marginBottom": "10px"}),
        ),
        dmc.Tooltip(
            multiline=True,
            width=220,
            withArrow=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            # transitionTimingFunction="ease",
            label="Enforce datatypes for columns in the table. This will convert the data in the column to the selected datatype. Furthermore, it will prevent the user from entering data that is not of the selected datatype.",
            children=dmc.Button("Enforce DataTypes", id="btn-enforce-dtypes",
                                style={"marginBottom": "10px"}),
        ),
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


        dmc.Button("Clean Data", id="clean-data-button"),
        # dmc.Button("Cancel", id="cancel-button", disabled=True),
        # dmc.Checkbox(id="auto-clean-checkbox", label="Auto Clean First?", checked=True),
        # dmc.Text(id="log-textbox"),


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
                    id="file-type-select",
                    style={"width": "80px"},
                    value="csv",
                    data=[
                        {"value": "csv", "label": "csv"},
                        {"value": "xml", "label": "xml"},
                        {"value": "html", "label": "html"},
                        # {"value": "xlsx", "label": "xlsx"},
                        # {"value": "pdf", "label": "pdf"},
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
