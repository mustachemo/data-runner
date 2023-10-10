from dash import html, dcc, dash_table
import dash_mantine_components as dmc
# import dash_bootstrap_components as dbc

layout = html.Div([  # This is the main layout of the app

    # Sidebar
    html.Div([
        html.Div([
            dmc.Image(  # This is the logo
                src="./assets/images/logo.jpeg", alt="USCS", width=40),
            dmc.Title(f"United States Cold Storage", order=5,),
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", "gap": "1rem", "marginBottom": "1rem", "borderBottom": "1px solid #ccc", 'padding': "1rem"}),

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

        dmc.Text("Messages", variant="subtle", style={"borderBottom": "1px dashed black", "paddingBottom": "5px"}),
        dmc.Alert("You have 50 empty cells and 23 corrupt cells", title="Warning!", color="yellow", style={"padding": "20px", "margin":"15px", "height": "150px", "borderRadius":"10px"}),





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
                # style_data={
                #     'backgroundColor': 'rgb(50, 50, 50)',
                #     'color': 'white'
                # },
                # fixed_rows={'headers':True, 'data':1}  # Fix header rows at the top
            ), parent_style={'maxWidth': '100%', 'maxHeight': '100%'}
        )

    ], className="main-content")

], className="app-container")
