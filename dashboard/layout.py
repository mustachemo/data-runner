from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([ # This is the main layout of the app
    dcc.Store(id='df-store'), # This will hold the data uploaded by the user in memory
    dbc.NavbarSimple( # This is the navigation bar
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

    dcc.Upload( # This is the upload button
        id='upload-data',
        children=html.Button('Upload File'), # This is the button that will be displayed
        style={},
        multiple=True # Allow multiple files to be uploaded
    ),
        
    dash_table.DataTable( # This is the table that will display the data
        id='editable-table',  # Assign an ID to the DataTable component
        editable=True,  # Enable editing,
        column_selectable="multi", # This enables column selection
        row_selectable='multi', # This enables row selection
        virtualization=True, # This enables virtualization, which allows large data sets to be rendered efficiently
        # selected_columns=[],
        # selected_rowss=[],
        sort_action='native', # This enables data to be sorted by the user
        filter_action='native', # This enables data to be filtered by the user
        row_deletable=True, # This enables users to delete rows
        style_table={'height': '70vh', 'width': '90%', 'overflowX': 'auto', 'margin': '1rem auto 0 auto'},
        style_cell={'textAlign': 'left'}, # left align text in columns for readability
        # fixed_rows={'headers':True, 'data':1}  # Fix header rows at the top
    ),
    html.Div([
        dcc.RadioItems(['csv', 'xsls','pdf', 'html', 'xml'],  id='radio-items', value='csv'), # This is the radio button that will allow the user to select the file type to download
        html.Button("Download", id="btn-download"), # This is the download button
        dcc.Download(id="download-file"), # This is the download action
    ], style={'margin': '1rem auto 0 auto', 'width': '90%'})
])