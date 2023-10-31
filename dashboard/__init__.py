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
    Output('initial-table-data', 'data'),
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
    Output('editable-table', 'style_data_conditional', allow_duplicate=True),
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

###################### CHECK CELLS DATATYPE [CLEANING OPERATION] ######################
@callback(
    Output('editable-table', 'data', allow_duplicate=True),
    # Output('editable-table', 'style_data_conditional', allow_duplicate=True),
    [Input('btn-check-cells-datatypes', 'n_clicks')],
    State('editable-table', 'columns'),
    State('editable-table', 'data'),
    prevent_initial_call=True
)
def show_noncomplient_data(n_clicks, columns, data):
    if columns is None or data is None or n_clicks is None:
        raise exceptions.PreventUpdate
    
    df = pd.DataFrame.from_dict(data)
    non_compliant_rows = set()  # To track rows with non-compliant data

    for col in columns:
        # Ensure the column has the 'type' key
        if 'type' not in col:
            continue

        if col['type'] == 'text':
            mask = df[col['name']].apply(lambda x: not isinstance(x, str))

        elif col['type'] == 'numeric':
            def is_numeric(val):
                if val is None:
                    return False    
                try:
                    # Remove hyphens (for negative numbers) and try to convert to float
                    float(val.replace('-', ''))
                    return True
                except (TypeError, ValueError):
                    return False

            mask = df[col['name']].apply(lambda x: not is_numeric(x))
    
        elif col['type'] == 'datetime':
            mask = df[col['name']].apply(lambda x: not isinstance(x, pd.Timestamp))
        else:
            continue

        # Find non-compliant indices and add them to the set
        non_compliant_indices = mask[mask].index.tolist()
        for idx in non_compliant_indices:
            non_compliant_rows.add(idx)  # Add row index to the set

    # Filter the dataframe to keep only rows with non-compliant data
    df_filtered = df[df.index.isin(non_compliant_rows)]
    print(df_filtered)

    if df_filtered.empty:
        return no_update
    
    # return df_filtered.to_dict('records'), []
    return df_filtered.to_dict('records')


###################### CLEAN CELLS DATATYPE [CLEANING OPERATION] highlighting ######################
@callback(
    Output('editable-table', 'style_data_conditional', allow_duplicate=True),
    [Input('editable-table', 'data')],
    State('editable-table', 'columns'),
    prevent_initial_call=True
)
def style_noncompliant_cells(data, columns):
    df = pd.DataFrame.from_dict(data)
    style_data_conditional = []

    for col in columns:
        if 'type' not in col:
            continue

        if col['type'] == 'text':
            mask = df[col['name']].apply(lambda x: not isinstance(x, str))
            color = '#6ee7b7'

        elif col['type'] == 'numeric':
            def is_numeric(val):
                if val is None:
                    return False    
                try:
                    float(val.replace('-', ''))
                    return True
                except (TypeError, ValueError):
                    return False

            mask = df[col['name']].apply(lambda x: not is_numeric(x))
            color = '#fde047'
    
        elif col['type'] == 'datetime':
            mask = df[col['name']].apply(lambda x: not isinstance(x, pd.Timestamp))
            color = '#c4b5fd'
        else:
            continue

        # Add styling information for non-compliant cells
        non_compliant_indices = mask[mask].index.tolist()
        for idx in non_compliant_indices:
            style_data_conditional.append({
                'if': {'row_index': idx, 'column_id': col['name']},
                'backgroundColor': color,
                'color': 'white'
            })

    return style_data_conditional




###################### RESET TABLE ######################
@callback(
    Output('editable-table', 'data', allow_duplicate=True),
    Output('editable-table', 'columns', allow_duplicate=True),
    # Output('editable-table', 'style_data_conditional', allow_duplicate=True),
    Input('btn-reset-table', 'n_clicks'),
    State('initial-table-data', 'data'),
    State('editable-table', 'columns'),

    prevent_initial_call=True
)
def reset_table(n_clicks, initial_data, initial_columns):
    if n_clicks is None:
        raise exceptions.PreventUpdate

    return initial_data, initial_columns


if __name__ == '__main__':
    app.run(debug=True)
