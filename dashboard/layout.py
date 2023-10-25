from dash import html, dcc, dash_table
import dash_mantine_components as dmc

layout = html.Div([  # This is the main layout of the app

    # This is the notification container
    # html.Div(id="notify-container"),

    # Sidebar
    html.Div([
        html.Div([
            dmc.Image(  # This is the logo
                src="./assets/images/logo.jpeg", alt="USCS", width=40),
            dmc.Title(f"United States Cold Storage", order=5,),
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", "gap": "1rem", "marginBottom": "1rem", "borderBottom": "1px solid #ccc", 'padding': "1rem"}),

        dmc.Text("Data Analysis", variant="subtle", style={
                 "borderBottom": "1px dashed black", "paddingBottom": "5px"}),
        dmc.Alert(id="alert-empty-and-corrupt-cells",
                  color="yellow"),

        dmc.Tooltip(
            withArrow=True,
            width=200,
            multiline=True,
            position="right",
            transition="fade",
            label="Opens a modal showing which columns have corrupt/missing cells and duplicate data",
            children=dmc.Button(
                "Detailed Analysis", id="btn-detailed-analysis", style={"marginBottom": "5px"}),
        ),

        dmc.Tooltip(
            multiline=True,
            width=200,
            withArrow=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            # transitionTimingFunction="ease",
            label="Opens a modal for cell higlighting options",
            children=dmc.Button("Highlight Cells", id="btn-higlight-cells",
                                style={"marginBottom": "5px"}),
        ),

        dmc.Modal(  # This is the modal that will open when the enforce datatypes button is clicked
            title="Choose options for cell highlighting",
            id="higlight-cells-modal",
            zIndex=10000,
            children=[
                dmc.Space(h=20),
                dmc.Checkbox(label="Highlight Empty/NaN/None Cells", id="highlight-empty-nan-null-cells-checkbox",
                             color="pink", checked=True),
                dmc.Space(h=10),
                dmc.Checkbox(
                    label="Highlight Datatype Enforced Columns", id="highlight-dtype-columns-cells-checkbox", color="pink", checked=True),
                dmc.Space(h=10),
                dmc.Group(
                    [
                        dmc.Button(
                            "Submit", id="higlight-modal-submit-button"),
                        dmc.Button(
                            "Close",
                            color="red",
                            variant="outline",
                            id="higlight-modal-close-button",
                        ),
                    ],
                    position="right",
                ),
            ],
        ),


        dmc.Text("User Preferences", variant="subtle", style={
                 "borderBottom": "1px dashed black", "paddingBottom": "5px"}),  # This is the preferences header
        dmc.Tooltip(  # This is enforce datatypes button
            multiline=True,
            width=200,
            withArrow=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            # transitionTimingFunction="ease",
            label="Enforce datatypes for each column in the table",
            children=dmc.Button("Enforce DataTypes", id="btn-enforce-dtypes",
                                style={"marginBottom": "5px"}),
        ),

        dmc.Modal(  # This is the modal that will open when the enforce datatypes button is clicked
            title="Select a column to enforce a datatype",
            id="enforce-dtypes-modal",
            zIndex=10000,
            children=[
                dmc.Space(h=20),
                html.Div(id='column-type-selector'),
                dmc.Space(h=20),
                dmc.Group(
                    [
                        dmc.Button("Submit", id="dtype-modal-submit-button"),
                        dmc.Button(
                            "Close",
                            color="red",
                            variant="outline",
                            id="dtype-modal-close-button",
                        ),
                    ],
                    position="right",
                ),
            ],
        ),

        dmc.Tooltip(  # This is enforce formatting button
            multiline=True,
            width=200,
            withArrow=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            # transitionTimingFunction="ease",
            label="Enforce formatting for cells in the table. This informs the cleaning function of specific formatting for selected columns. The cleaning function will be able to pick up on these formats and clean the data accordingly.",
            children=dmc.Button("Enforce Formatting", id="btn-enforce-format",
                                style={"marginBottom": "20px"}),
        ),


        dmc.Text("Cleaning Operations", variant="subtle", style={
                 "borderBottom": "1px dashed black", "paddingBottom": "5px"}),


        dmc.Tooltip(
            withArrow=True,
            width=200,
            multiline=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            label="Distinguish and iterate over empty and corrupt cells",
            children=dmc.Button(
                "Check Empty/Corrupt Cells", id="btn-check-empty-corrupt-cells", style={"marginBottom": "5px"}),
        ),
        dmc.Modal(  # This is the modal that will open when the enforce datatypes button is clicked
            title="Show all empty/corrupt cells",
            id="check-empty-corrupt-cells-modal",
            zIndex=10000,
            children=[
                dmc.Space(h=20),
                dash_table.DataTable(  # This is the table that will display the data
                    id='empty-corrupt-editable-table',  # Assign an ID to the DataTable component
                    editable=True,  # Enable editing,
                    # column_selectable="multi",  # This enables column selection
                    # row_selectable='multi',  # This enables row selection
                    # virtualization=True, # Enabling virtualization causes the table to not render properly
                    # selected_columns=[],
                    # selected_rowss=[],
                    sort_action='native',  # This enables data to be sorted by the user
                    filter_action='native',  # This enables data to be filtered by the user
                    row_deletable=True,  # This enables users to delete rows
                    style_table={'minHeight': '75vh', 'height': '75vh', 'maxWidth': '100%',
                                 'overflowY': 'auto', 'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'rgb(224,241,255)',
                        'color': 'rgb(12,127,218)'
                    },
                    style_cell_conditional=()
                    # style_data={
                    #     'backgroundColor': 'rgb(50, 50, 50)',
                    #     'color': 'white'
                    # },
                    # fixed_rows={'headers': True, 'data': 0}
                ),
                dmc.Space(h=20),
                dmc.Group(
                    [
                        dmc.Button(
                            "Submit", id="check-empty-modal-submit-button"),
                        dmc.Button(
                            "Close",
                            color="red",
                            variant="outline",
                            id="check-empty-modal-close-button",
                        ),
                    ],
                    position="right",
                ),
            ],
        ),

        dmc.Tooltip(
            withArrow=True,
            width=200,
            multiline=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            label="Removes duplicate rows from the imported data",
            children=dmc.Button(
                "Remove Duplicates", id="btn-remove-duplicates", style={"marginBottom": "5px"}),
        ),

        dmc.Tooltip(
            withArrow=True,
            width=200,
            multiline=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            label="Distinguish cells that don't match their columns enforced datatypes, set in user preferences",
            children=dmc.Button(
                "Check Cells Datatypes", id="btn-check-cells-datatypes", style={"marginBottom": "5px"}),
        ),

        dmc.Tooltip(
            withArrow=True,
            width=200,
            multiline=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            label="Distinguish cells that don't match their columns enforced formatting, set in user preferences",
            children=dmc.Button(
                "Check Cells Formatting", id="btn-check-cells-formatting", style={"marginBottom": "5px"}),
        ),
        dmc.Tooltip(
            withArrow=True,
            width=200,
            multiline=True,
            position="right",
            transition="fade",
            transitionDuration=300,
            label="Check all cells for any issues",
            children=dmc.Button(
                "Clean All", id="btn-clean-all", style={"marginBottom": "20px"}, color="red"),
        ),
        # dmc.Button("Cancel", id="cancel-button", disabled=True),
        # dmc.Checkbox(id="auto-clean-checkbox", label="Auto Clean First?", checked=True),
        # dmc.Text(id="log-textbox"),



    ], className="sidebar"),




    # Main content
    html.Div([
        html.Div([
            dmc.NotificationsProvider(
                html.Div(
                    [
                        html.Div(id="notifications-container"),
                        html.Div(  # Corrected children to html.Div
                            dmc.Tooltip(
                                withArrow=True,
                                width=200,
                                multiline=True,
                                position="right",
                                transition="fade",
                                transitionDuration=300,
                                label="Multiple file uploads will be combined into one table, duplicate rows removed, and mismatched columns ignored.",
                                children=[
                                    dcc.Upload(
                                        id='upload-data',
                                        children=dmc.Button("Upload File", style={
                                                            "backgroundColor": "#0C7FDA"}),
                                        multiple=True
                                    ),
                                ],
                            ),
                        ),
                    ]
                ),
            ),
            html.Div([

                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Empty/Corrupt Cells: Cells that are empty, NaN, or None",
                    children=html.Div(style={
                        'display': 'inline-block',
                        'width': '20px',
                        'height': '20px',
                        'backgroundColor': 'tomato',
                        "margin": "0.5rem",
                    })),

                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Cells with numeric datatype enforced",
                    children=html.Div(style={
                        'display': 'inline-block',
                        'width': '20px',
                        'height': '20px',
                        'backgroundColor': 'lightgreen',
                        'margin': '0.5rem',
                    })),

                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Cells with datetime datatype enforced",
                    children=html.Div(style={
                        'display': 'inline-block',
                        'width': '20px',
                        'height': '20px',
                        'backgroundColor': 'lightyellow',
                        'margin': '0.5rem',
                    })),

            ], style={"display": "flex", "backgroundColor": "grey"}),

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
                # column_selectable="multi",  # This enables column selection
                # row_selectable='multi',  # This enables row selection
                # virtualization=True, # Enabling virtualization causes the table to not render properly
                # selected_columns=[],
                # selected_rowss=[],
                sort_action='native',  # This enables data to be sorted by the user
                filter_action='native',  # This enables data to be filtered by the user
                row_deletable=True,  # This enables users to delete rows
                style_table={'minHeight': '75vh', 'height': '75vh', 'maxWidth': '100%',
                             'overflowY': 'auto', 'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(224,241,255)',
                    'color': 'rgb(12,127,218)'
                },
                style_cell_conditional=()
                # style_data={
                #     'backgroundColor': 'rgb(50, 50, 50)',
                #     'color': 'white'
                # },
                # fixed_rows={'headers': True, 'data': 0}
            ), parent_style={'maxWidth': '100%', 'maxHeight': '100%'}
        )

    ], className="main-content")

], className="app-container")
