from dash import Dash, Input, Output, State, callback, exceptions
import pandas as pd

from dashboard.utils.datacleaner import DataCleaner as dc
import dashboard.utils.handleFile as HandleFile
from .layout import layout

# This is the data handler object (see dashboard/utils/datahandler.py)
dc = dc()
# This is the main app object
app = Dash(__name__)
# Improves load time by not loading all callbacks at once. 5-10% improvement
#app.config.suppress_callback_exceptions = True

app.layout = layout


###################### UPLOAD FILE ######################
@callback(
    Output('editable-table', 'data'),
    Output('editable-table', 'columns'),
    State('editable-table', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True,
)
def upload_file(prevData, files, fileNames):
    if files is None:
        raise exceptions.PreventUpdate

    return HandleFile.importFiles(prevData, files, fileNames)


###################### DOWNLOAD FILE ######################
@callback(  # This is a callback that will download the file
    Output("download-file", "data"),
    Input("btn-download", "n_clicks"),
    State('editable-table', 'data'),
    State('editable-table', 'columns'),
    State('file-type-select', 'value'),
    prevent_initial_call=True,
)
def download_file(_, data, columns, fileType):
    return HandleFile.exportFile(data, columns, fileType)


###################### HIGHLIGHT COLUMNS ######################
@callback(  # This is a callback that will highlight the selected columns
    Output('editable-table', 'style_data_conditional'),
    Input('editable-table', 'selected_columns')
    # Input('editable-table', 'selected_rows')
)
def highlight_column(selected_columns):
    styles = []

    if selected_columns:
        styles.extend([{'if': {'column_id': col}, 'background_color': '#D2F3FF'}
                       for col in selected_columns])

    # if selected_rows:
    #     styles.extend([{'if': {'row_index': row}, 'background_color': '#7FFF7F'} for row in selected_rows])

    return styles


if __name__ == '__main__':
    app.run(debug=True)
