from dash import Dash, Input, Output, State, callback, callback_context, exceptions, dcc, html, exceptions, DiskcacheManager, no_update
import dash_mantine_components as dmc
import os
import pandas as pd
import diskcache
from dash_iconify import DashIconify

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

###################### UPLOAD FILE Notification ######################
@callback(
    Output("notifications-container", "children"),
    Input("upload-data", "filename"),
    prevent_initial_call=True,
)

def show(filenames):
    if not filenames:
        return dmc.Notification(
            id="upload-notifcation",
            action="show",
            # autoClose=100000,
            message="Upload Failed",
            icon=DashIconify(icon="ic:round-error"),
        )
    
    file_types = {'.csv', '.xlsx', ".xls", ".xlsm" '.html', '.xml'}
    for filename in filenames:
        ext = os.path.splitext(filename)[1].lower()
        if ext in file_types:
            return dmc.Notification(
                id="upload-notifcation",
                action="show",
                # autoClose=100000,
                message="File Uploaded!",
                icon=DashIconify(icon="ic:round-upload"),
            )

    return dmc.Notification(
        id="upload-notifcation",
        action="show",
        # autoClose=100000,
        message="Upload Failed!",
        icon=DashIconify(icon="ic:round-error"),
    )

###################### Data Analytics ######################
@callback(
    Output('alert-empty-and-corrupt-cells', 'children'),
    Input('editable-table', 'data', )
)
def check_number_of_empty_and_corrupt_cells(data):
    if data is None:
        raise exceptions.PreventUpdate

    return DataAnalysis.get_data_analysis(data)

###################### FILTER SYNTAX MODAL #################
@callback(
    Output("filter-syntax-modal", "opened"),
    Input("filter-syntax-btn", "n_clicks"),
    State("filter-syntax-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    return not opened

###################### HIGHLIGHT CELLS (OPEN MODAL) ######################
@callback(
    Output("higlight-cells-modal", "opened"),
    Input("btn-higlight-cells", "n_clicks"),
    Input("higlight-modal-submit-button", "n_clicks"),
    Input("higlight-modal-close-button", "n_clicks"),
    State("higlight-cells-modal", "opened"),
    prevent_initial_call=True,
)
def higlight_cells_modal(nc1, nc2, nc3, opened):
    return not opened


###################### HIGHLIGHT CELLS (SUBMIT MODAL) ######################
@callback(
    Output('editable-table', 'style_data_conditional'),
    Input("higlight-modal-submit-button", "n_clicks"),
    State('highlight-empty-nan-null-cells-checkbox', 'checked'),
    State('highlight-dtype-columns-cells-checkbox', 'checked'),
    State("editable-table", "columns"),
    prevent_initial_call=True,
)
def highlight_cells(submit_btn, highlight_empty_cells, highlight_dtype_cells, columns):
    if not columns:
        raise exceptions.PreventUpdate

    new_highlighting = []

    if highlight_empty_cells:
        new_highlighting.extend(
            DataAnalysis.higlight_empty_nan_null_cells(columns))

    if highlight_dtype_cells:
        new_highlighting.extend(
            DataAnalysis.generate_dtype_highlighting(columns))

    if submit_btn:
        return new_highlighting


###################### REMOVE DUPLICATE ROWS ######################
@callback(
    Output('editable-table', 'data'),
    # Output('notify-container', 'children'),
    State('editable-table', 'data'),
    Input('btn-remove-duplicates', 'n_clicks')
)
def remove_duplicate_rows(data, n_clicks):
    if data is None and n_clicks is None:
        raise exceptions.PreventUpdate

    df = pd.DataFrame.from_dict(data)
    df.drop_duplicates(inplace=True)
    return df.to_dict('records')

    # success_notification = dmc.Notification(
    #     id="my-notification",
    #     title="Data loaded",
    #     message="The process has started.",
    #     color="green",
    #     action="show",
    #     icon=DashIconify(icon="akar-icons:circle-check"),
    # )
    # return DataCleaner.remove_duplicate_rows(data, n_clicks), success_notification
    # return DataCleaner.remove_duplicate_rows(data, n_clicks)


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
    Input("dtype-modal-close-button", "n_clicks"),
    Input("dtype-modal-submit-button", "n_clicks"),
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
    Input('dtype-modal-submit-button', 'n_clicks'),
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
