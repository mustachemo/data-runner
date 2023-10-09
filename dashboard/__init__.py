from dash import Dash, Input, Output, State, callback, callback_context, exceptions, dcc, html, exceptions, DiskcacheManager
import dash_bootstrap_components as dbc
import pandas as pd
import diskcache

import dashboard.utils.datacleaner as DataCleaner
import dashboard.utils.handleFile as HandleFile
from .layout import layout

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheManager(cache)

# This is the main app object
app = Dash(__name__)
# Improves load time by not loading all callbacks at once. 5-10% improvement
# app.config.suppress_callback_exceptions = True

app.layout = layout

# region handleFile

###################### UPLOAD FILE ######################


@callback(
    Output('editable-table', 'data', allow_duplicate=True),
    Output('editable-table', 'columns', allow_duplicate=True),
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
@callback(
    Output("download-file", "data"),
    Input("btn-download", "n_clicks"),
    State('editable-table', 'data'),
    State('editable-table', 'columns'),
    State('file-type-select', 'value'),
    prevent_initial_call=True,
)
def download_file(_, data, columns, fileType):
    return HandleFile.exportFile(data, columns, fileType)

# endregion

# region design

###################### HIGHLIGHT COLUMNS ######################


@callback(
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


# endregion

# region datacleaner

@app.long_callback(
    Output("editable-table", "data"),
    Output("log-textbox", "children"),
    Input("clean-data-button", "n_clicks"),
    State("editable-table", "data"),
    State("editable-table", "columns"),
    State("auto-clean-checkbox", "checked"),
    running=[(Output("clean-data-button", "disabled"), True, False),
             (Output("cancel-button", "disabled"), False, True)
             ],
    cancel=[Input("cancel-button", "n_clicks")],
    manager=long_callback_manager,
    prevent_initial_call=True,
)
def cleanData(_, data, columns, isAutoClean):
    # todo manual clean
    # todo get and use user preferences
    # todo clean up logging
    # reconsider what to report based on frontend needs
    userPreferences = {"*": "int"}
    if (isAutoClean):
        data, message, changedCells, emptyCells, needsAttention = DataCleaner.cleanDataAuto(
            data, columns, userPreferences)
        message = f"changed{changedCells}, empty{emptyCells}, needsAttention{needsAttention}"
        print(message)
        return data, message

    print("Not implemented")
    raise exceptions.NonExistentEventException

# endregion


###################### ENFORCE DATATYPES (OPEN MODAL) ######################
@callback(
    Output("enforce-dtypes-modal", "opened"),
    Input("btn-enforce-dtypes", "n_clicks"),
    Input("modal-close-button", "n_clicks"),
    Input("modal-submit-button", "n_clicks"),
    State("enforce-dtypes-modal", "opened"),
    prevent_initial_call=True,
)
def modal_demo(nc1, nc2, nc3, opened):
    return not opened


###################### ENFORCE DATATYPES (FILL MODAL WITH COLUMNS) ######################
@callback(
    Output("column-type-selector", "children"),
    Input("enforce-dtypes-modal", "opened"),
    State("editable-table", "columns"),
    prevent_initial_call=True,
)
def populate_datatype_selection(opened, columns):
    if not opened or not columns:
        raise exceptions.PreventUpdate

    column_list = [col['name']
                   for col in columns]  # Get column names from DataTable
    data_type_options = ["numeric", "text",
                         "any", "datetime"]  # Data type options

    children = []  # This is the list of children that will be returned, each child is a row in the modal
    for col in column_list:
        dropdown = dcc.Dropdown(  # This is the dropdown for each column
            id={'type': 'datatype-dropdown', 'index': col},
            options=[{'label': dt, 'value': dt} for dt in data_type_options],
            value=None,
            placeholder="Select data type",
            style={'width': '9rem'}
        )
        children.append(html.Div([html.Label(col), dropdown], style={
                        "display": "flex", "justifyContent": "space-between", "alignItems": "center", "padding": "0.5rem", "borderBottom": "1px solid #000"}))

    return children


if __name__ == '__main__':
    app.run(debug=True)
