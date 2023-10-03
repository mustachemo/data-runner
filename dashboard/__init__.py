from dash import Dash, Input, Output, State, callback, callback_context, exceptions
import dash_bootstrap_components as dbc
import pandas as pd

from dashboard.utils.datahandler import DataHandler
from .layout import layout

data_handler = DataHandler(pd.DataFrame()) # This is the data handler object (see dashboard/utils/datahandler.py)
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) # This is the main app object
app.config.suppress_callback_exceptions = True # Improves load time by not loading all callbacks at once. 5-10% improvement

app.layout = layout

@callback( # This is a callback that will download the file
    Output("download-file", "data"),
    [Input("btn-download", "n_clicks")],
    [State('radio-items', 'value'),
     State('editable-table', 'data'),
     State('editable-table', 'columns')],
    prevent_initial_call=True,
)
def download_specific_files(_, fileType, dataTableData, current_columns):
    return data_handler.download_specific_files(_, fileType, dataTableData, current_columns)



@app.callback( # This is a callback that will highlight the selected columns
    Output('editable-table', 'style_data_conditional'),
    Input('editable-table', 'selected_columns')
    # Input('editable-table', 'selected_rows')
)
def highlight_column(selected_columns):
    return data_handler.highlight_column(selected_columns)


@callback( # This is a callback that will upload the file and cache it
    Output('df-store', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def upload_file_and_cache(list_of_contents, list_of_names, list_of_dates):
    return data_handler.upload_file_and_cache(list_of_contents, list_of_names, list_of_dates)


@callback( # This is a callback that will update the table with the data from the cache
    Output('editable-table', 'data'),
    Output('editable-table', 'columns'),
    Input('df-store', 'data')
)
def update_table(data):
    return data_handler.update_table(data)

if __name__ == '__main__':
    app.run(debug=True)
