from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    dcc.Store(id='df-store'), # This will hold the data uploaded by the user
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
        virtualization=True, # This enables virtualization, which allows large data sets to be rendered efficiently
    
        # selected_columns=[],
        # selected_rowss=[],
        sort_action='native',
        filter_action='native',
        row_deletable=True,
        style_table={'height': '70vh', 'width': '90%', 'overflowX': 'auto', 'margin': '1rem auto 0 auto'},
        style_cell={'textAlign': 'left'}, # left align text in columns for readability
        # fixed_rows={'headers':True, 'data':1}  # Fix header rows at the top
    ),
    dcc.RadioItems(['csv', 'xsls','pdf', 'html', 'xml'],  id='radio-items', value='csv'), 
    html.Button("Download", id="btn-download"),
    dcc.Download(id="download-file"),
])