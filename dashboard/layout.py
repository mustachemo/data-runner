from dash import html, dcc, dash_table
import dash_mantine_components as dmc
from dash_iconify import DashIconify

layout = dmc.NotificationsProvider(html.Div([  # This is the main layout of the app

    # This is the notification container
    html.Div(id="notifications-container"),
    dcc.Store(id='initial-table-data'),
    dcc.Store(id='initial-table-columns'),
    dcc.Store(id='noncomplient-indices'),
    dcc.Store(id='formatting-store'),

    # Sidebar
    # Sidebar
    html.Div([
        html.Div([
            dmc.Image(  # This is the logo
                src="./assets/images/logo.jpeg", alt="USCS", width=40),
            dmc.Title(f"United States Cold Storage", order=5,),
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", "gap": "1rem", "marginBottom": "1rem", "borderBottom": "1px solid #ccc", 'padding': "1rem"}),
        html.Div(id='store-output'),
        html.Div([
            dmc.Menu([
                dmc.MenuLabel("Data Analysis", style={"padding-left": "5px"}),
                # dmc.MenuDivider(style={"width": 200, "padding-left": "5px"}),
                dmc.Alert(id="alert-empty-and-corrupt-cells", color="yellow"),
                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    label="Opens a modal showing which columns have corrupt/missing cells and duplicate data",
                    children=dmc.Button("Detailed Analysis", id="btn-detailed-analysis", variant="subtle", leftIcon=DashIconify(icon="bx:data"),),
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
                    children=dmc.Button("Highlight Cells", id="btn-higlight-cells", variant="subtle", leftIcon=DashIconify(icon="bx:highlight"),),
                ),
                dmc.Modal(  # This is the modal that will open when the highlight cells button is clicked
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
                dmc.Space(h=20),
                dmc.MenuLabel("User Preferences", style={"padding-left": "5px"}),
                dmc.Tooltip(  # This is enforce datatypes button
                    multiline=True,
                    width=200,
                    withArrow=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    # transitionTimingFunction="ease",
                    label="Enforce datatypes for each column in the table",
                    children=dmc.Button("Enforce Datatypes", id="btn-enforce-dtypes", variant="subtle", leftIcon=DashIconify(icon="material-symbols:data-check"),)
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
                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Distinguish cells that don't match their columns enforced formatting, set in user preferences",
                    children=dmc.Button("Enforce Formatting", id="btn-enforce-format", variant="subtle", leftIcon=DashIconify(icon="streamline:interface-edit-write-2-change-document-edit-modify-paper-pencil-write-writing"),)
                ),
                dmc.Modal(  # This is the modal that will open when the enforce formatting button is clicked
                    title="Input a specified format for each column",
                    id="enforce-formatting-modal",
                    zIndex=10000,
                    size="70rem",
                    children=[
                        html.Div(id='column-format-selector'),
                        dmc.Space(h=20),
                        dmc.Group(
                            [
                                dmc.Button("Submit", id="formatting-modal-submit-button"),
                                dmc.Button(
                                    "Close",
                                    color="red",
                                    variant="outline",
                                    id="formatting-modal-close-button",
                                ),
                            ],
                            position="right",
                        ),
                    ],
                ),
                dmc.Space(h=20),
                dmc.MenuLabel("Cleaning Operations", style={"padding-left": "5px"}),
                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Distinguish and iterate over empty and corrupt cells",
                    children=dmc.Button("Check Empty/Corrupt Cells", id="btn-check-empty-corrupt-cells", variant="subtle", leftIcon=DashIconify(icon="iconoir:info-empty"),)
                ),
                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Removes duplicate rows from the imported data",
                    children=dmc.Button("Remove Duplicates", id="btn-remove-duplicates", variant="subtle", leftIcon=DashIconify(icon="bx:duplicate"),)
                ),

                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Distinguish cells that don't match their columns enforced datatypes, set in user preferences",
                    children=dmc.Button("Check Cells Datatypes", id="btn-check-cells-datatypes", variant="subtle", leftIcon=DashIconify(icon="gg:check-o"),)
                ),

                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Distinguish cells that don't match their columns enforced formatting, set in user preferences",
                    children=dmc.Button("Check Cells Formatting", id="btn-check-cells-formatting", variant="subtle", leftIcon=DashIconify(icon="mdi:checkbox-outline"),),
                ),
                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Check all cells for any issues",
                    children=dmc.Button("Clean All", id="btn-clean-all", variant="subtle", color="red", leftIcon=DashIconify(icon="material-symbols:cleaning-services-outline"),),
                ),
            ]),
        ], style={"fontSize": "26px"}),
    ], className="sidebar"),




    # Main content
    html.Div([
        html.Div([

            html.Div(
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
                            children=dmc.Button("Upload File", style={"backgroundColor": "#0C7FDA"}),
                            multiple=True
                        ),
                    ],
                ),
            ),


            dmc.Button("Reset Table", id="btn-reset-table", style={"backgroundColor": "#0C7FDA"}),
            html.Div(id="btn-confirm-changes-container"),

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
                        'backgroundColor': '#f87171',
                        "margin": "0.5rem",
                    })),

                dmc.Tooltip(
                    withArrow=True,
                    width=200,
                    multiline=True,
                    position="right",
                    transition="fade",
                    transitionDuration=300,
                    label="Cells with text datatype enforced",
                    children=html.Div(style={
                        'display': 'inline-block',
                        'width': '20px',
                        'height': '20px',
                        'backgroundColor': '#fde047',
                        'margin': '0.5rem',
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
                        'backgroundColor': '#6ee7b7',
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
                        'backgroundColor': '#c4b5fd',
                        'margin': '0.5rem',
                    })),

            ], style={"display": "flex", "backgroundColor": "grey"}),

            html.Div([  # This is the dropdown and download button
                dmc.Select(
                    id="file-type-select",
                    style={"width": "80px"},
                    value="csv",
                    zIndex=10000,
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
                style_cell={'textAlign': 'left', 'overflow': 'hidden',
                            'textOverflow': 'ellipsis', 'minWidth':'200px',
                            'width': '100%', 'maxWidth':'400px'},
                style_header={
                    'backgroundColor': 'rgb(224,241,255)',
                    'color': 'rgb(12,127,218)'
                },
                style_cell_conditional=(),
                # style_data_conditional=()
                # style_data={
                #     'backgroundColor': 'rgb(50, 50, 50)',
                #     'color': 'white'
                # },
                # fixed_rows={'headers': True, 'data': 0}
            ), parent_style={'maxWidth': '100%', 'maxHeight': '100%'}
        )

    ], className="main-content")

], className="app-container"))
