from dash import Dash, Input, Output, State, callback, callback_context, exceptions, dcc, html, exceptions, DiskcacheManager
import dash_mantine_components as dmc
import pandas as pd
import diskcache

import dashboard.utils.dataCleaner as DataCleaner
import dashboard.utils.handleFile as HandleFile
import dashboard.utils.userPreferences as UserPreferences
import dashboard.utils.dataAnalysis as DataAnalysis
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
    Output('editable-table', 'fixed_rows'),
    State('editable-table', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True,
)
def upload_file(prevData, files, fileNames):
    if files is None:
        raise exceptions.PreventUpdate

    return HandleFile.importFiles(prevData, files, fileNames)


###################### CHECK NUMBER OF EMPTY AND CORRUPT CELLS WHEN FILE IS UPLOADED ######################
@callback(
    Output('alert-empty-and-corrupt-cells', 'children'),
    Input('editable-table', 'data', )
)
def check_number_of_empty_and_corrupt_cells(data):
    if data is None:
        raise exceptions.PreventUpdate

    return DataAnalysis.get_data_analysis(data)


###################### REMOVE DUPLICATE ROWS ######################
@callback(
    Output('editable-table', 'data'),
    State('editable-table', 'data'),
    Input('btn-remove-duplicates', 'n_clicks')
)
def remove_duplicate_rows(data, n_clicks):
    if data is None:
        raise exceptions.PreventUpdate

    return DataCleaner.remove_duplicate_rows(data, n_clicks)


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


# @callback(
#     Output('editable-table', 'style_data_conditional'),
#     Input('editable-table', 'selected_columns')
#     # Input('editable-table', 'selected_rows')
# )
# def highlight_column(selected_columns):
#     styles = []

#     if selected_columns:
#         styles.extend([{'if': {'column_id': col}, 'background_color': '#D2F3FF'}
#                        for col in selected_columns])

#     # if selected_rows:
#     #     styles.extend([{'if': {'row_index': row}, 'background_color': '#7FFF7F'} for row in selected_rows])

#     return styles


# endregion

# region datacleaner

# @app.long_callback(
#     Output("editable-table", "data"),
#     Output("log-textbox", "children"),
#     Input("clean-data-button", "n_clicks"),
#     State("editable-table", "data"),
#     State("editable-table", "columns"),
#     State("auto-clean-checkbox", "checked"),
#     running=[(Output("clean-data-button", "disabled"), True, False),
#              (Output("cancel-button", "disabled"), False, True)
#              ],
#     cancel=[Input("cancel-button", "n_clicks")],
#     manager=long_callback_manager,
#     prevent_initial_call=True,
# )
# def cleanData(_, data, columns, isAutoClean):
#     # todo manual clean
#     # todo get and use user preferences
#     # todo clean up logging
#     # reconsider what to report based on frontend needs
#     userPreferences = {"*": "int"}
#     if (isAutoClean):
#         data, message, changedCells, emptyCells, needsAttention = DataCleaner.cleanDataAuto(
#             data, columns, userPreferences)
#         message = f"changed{changedCells}, empty{emptyCells}, needsAttention{needsAttention}"
#         print(message)
#         return data, message

#     print("Not implemented")
#     raise exceptions.NonExistentEventException

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
def enforce_dtypes_modal(nc1, nc2, nc3, opened):
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
        return dmc.Text("Upload a file to enforce datatypes!", style={"color": "black", "fontWeight": "bold", "textAlign": "center"})

    return UserPreferences.populate_datatype_selection(opened, columns)


###################### ENFORCE DATATYPES (SUBMIT MODAL) ######################
@callback(
    Output('editable-table', 'columns'),
    Input('modal-submit-button', 'n_clicks'),
    State('column-type-selector', 'children'),
    State('editable-table', 'columns'),
    prevent_initial_call=True
)
def update_column_datatypes(_, modal_children, columns):
    if not columns:
        raise exceptions.PreventUpdate

    dropdown_values = UserPreferences.extract_dropdown_values(modal_children)

    # We are able to iterate over columns and dropdown_values simultaneously because they are both in the same order
    for col, dtype in zip(columns, dropdown_values):
        if dtype:
            col['type'] = dtype

    return columns


if __name__ == '__main__':
    app.run(debug=True)
