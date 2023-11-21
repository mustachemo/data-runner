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
import json
import re

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheManager(cache)

# This is the main app object
app = Dash(__name__, suppress_callback_exceptions=True)
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
    Output('notifications-container', 'children'),
    State('editable-table', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True,
)
def upload_file(prevData, files, fileNames):
    if files is None:
        raise exceptions.PreventUpdate



    return HandleFile.importFiles(prevData, files, fileNames)

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
    Output('notifications-container', 'children', allow_duplicate=True),
    State('editable-table', 'data'),
    Input('btn-remove-duplicates', 'n_clicks'),
    prevent_initial_call=True
)
def remove_duplicate_rows(data, n_clicks):
    if data is None and n_clicks is None:
        raise exceptions.PreventUpdate

    df = pd.DataFrame.from_dict(data)
    df.drop_duplicates(inplace=True)

    # Count how many rows were removed
    rows_removed = len(data) - len(df)

    if rows_removed == 0:
        notification = dmc.Notification(
            title="No duplicate rows found!",
            id="simple-notify",
            color="yellow",
            action="show",
            autoClose=3000,
            message="",
            icon=DashIconify(icon="akar-icons:circle-alert")
        )
        return no_update, notification

    else: 
        notification = dmc.Notification(
            title="Duplicate rows removed!",
            id="simple-notify",
            color="yellow",
            action="show",
            autoClose=3000,
            message=f'{rows_removed} rows removed',
            icon=DashIconify(icon="akar-icons:circle-check"),
        )

        return df.to_dict('records'), notification


###################### DOWNLOAD FILE ######################
@callback(
    Output("download-file", "data"),
    Output("notifications-container", "children", allow_duplicate=True),
    Input("btn-download", "n_clicks"),
    State('editable-table', 'data'),
    State('editable-table', 'columns'),
    State('file-type-select', 'value'),
    prevent_initial_call=True,
)
def download_file(_, data, columns, fileType):
    if (data == None or columns == None):
        print("Nothing to export")
        raise exceptions.PreventUpdate

    notification = dmc.Notification(
        title="File Exported Successfuly!",
        id="simple-notify",
        color="green",
        action="show",
        autoClose=3000,
        message='',
        icon=DashIconify(icon="akar-icons:circle-alert"),
    )

    return HandleFile.exportFile(data, columns, fileType), notification

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

###################### ENFORCE FORMATTING (OPEN MODAL) ######################
@callback(
    Output("enforce-formatting-modal", "opened"),
    Input("btn-enforce-format", "n_clicks"),
    Input("formatting-modal-close-button", "n_clicks"),
    Input("formatting-modal-submit-button", "n_clicks"),
    State("enforce-formatting-modal", "opened"),
    prevent_initial_call=True,
)
def enforce_dtypes_modal(nc1, nc2, nc3, opened):
    return not opened

###################### ENFORCE FORMATTING (FILL MODAL WITH COLUMNS) ######################
@callback(
    Output("column-format-selector", "children"),
    Input("enforce-formatting-modal", "opened"),
    State("editable-table", "columns"),
    State('formatting-store', 'data'),
    prevent_initial_call=True,
)
def populate_format_selection(opened, columns, formatting_options):
    if not opened or not columns:
        return dmc.Text("Upload a file to enforce formatting!", style={"color": "black", "fontWeight": "bold", "textAlign": "center"})

    formatting_options = json.loads(formatting_options) if formatting_options else None

    children = []
    children.append(UserPreferences.create_regex_instructional_area())
    children.append(dmc.Space(h=20))

    for col_details in columns:
        col_name = col_details['name']

        # Retrieve the format from the stored formatting if it exists, otherwise set to None
        placeholder_value = formatting_options.get(col_name, None) if formatting_options else None

        input_text = dmc.TextInput(
            id={'type': 'format-input', 'index': col_name},
            value=placeholder_value,
            placeholder="Enter format",
            style={'width': '20rem'}
        )

        
        children.append(
            html.Div(
                [html.Label(col_name), input_text],
                style={"display": "flex", "justifyContent": "space-between",
                       "alignItems": "center", "padding": "0.5rem", "borderBottom": "1px solid #000"}
            )
        )

    return children

###################### ENFORCE FORMATTING (SUBMIT MODAL) ######################
@callback(
    Output('formatting-store', 'data'),
    Input('formatting-modal-submit-button', 'n_clicks'),
    State('column-format-selector', 'children'),
    State('editable-table', 'columns'),
    prevent_initial_call=True
)
def update_column_formatting(_, modal_children, columns):
    if not columns:
        raise exceptions.PreventUpdate

    format_values = UserPreferences.extract_input_values(modal_children)

    # Create a dictionary with column names as keys and formatting options as values
    column_formats = {
        col['name']: fmt_val for col, fmt_val in zip(columns, format_values) if fmt_val
    }

    print(f'Formatting options: {column_formats}')

    return json.dumps(column_formats)



###################### CHECK CELLS FORMATTING [CLEANING OPERATION] ######################
@callback(
    Output('editable-table', 'data', allow_duplicate=True),
    Output('notifications-container', 'children', allow_duplicate=True),
    Output('btn-confirm-changes-container', 'children', allow_duplicate=True),
    [Input('btn-check-cells-formatting', 'n_clicks')],
    State('formatting-store', 'data'),  # State to hold formatting options
    State('editable-table', 'columns'),
    State('editable-table', 'data'),
    prevent_initial_call=True
)
def show_noncompliant_format_data(n_clicks, formatting_store_data, columns, data):
    if columns is None or data is None or n_clicks is None:
        raise exceptions.PreventUpdate
    
    if formatting_store_data is None:
        notification = dmc.Notification(
            title="No formatting options found!",
            id="simple-notify",
            color="yellow",
            action="show",
            message="",
            autoClose=3000,
            icon=DashIconify(icon="akar-icons:circle-alert")
        )
        return no_update, notification, no_update
    
    # Load the stored formatting options
    formatting_options = json.loads(formatting_store_data)
    df = pd.DataFrame.from_dict(data)
    non_compliant_rows = set()  # To track rows with non-compliant data

    for col in columns:
        col_name = col['name']
        # Ensure the column has a formatting pattern stored
        if col_name in formatting_options:
            pattern = formatting_options[col_name]
            regex = re.compile(pattern)

            # Find non-compliant indices and add them to the set
            non_compliant_indices = df[col_name].apply(lambda x: not regex.match(str(x)) if x else False)
            non_compliant_rows.update(non_compliant_indices[non_compliant_indices].index.tolist())

    # Filter the dataframe to keep only rows with non-compliant data
    df_filtered = df.loc[list(non_compliant_rows)]

    if df_filtered.empty:
        print("No format non-compliant data found")
        
        notification = dmc.Notification(
            title="No format non-complient data found!",
            id="simple-notify",
            color="yellow",
            action="show",
            message="",
            autoClose=3000,
            icon=DashIconify(icon="akar-icons:circle-alert")
        )
        return no_update, notification, no_update
    
    confirm_button = dmc.Button("Confirm Changes", id="btn-confirm-changes", style={"backgroundColor": "#12B886"})
            
    return df_filtered.to_dict('records'), [], confirm_button


###################### CHECK CELLS DATATYPE [CLEANING OPERATION] ######################
@callback(
    Output('editable-table', 'data', allow_duplicate=True),
    Output('noncomplient-indices', 'data'),
    Output('notifications-container', 'children', allow_duplicate=True),
    Output('btn-confirm-changes-container', 'children', allow_duplicate=True),
    [Input('btn-check-cells-datatypes', 'n_clicks')],
    State('editable-table', 'columns'),
    State('editable-table', 'data'),
    prevent_initial_call=True
)
def show_noncomplient_dtype_data(n_clicks, columns, data):
    if columns is None or data is None or n_clicks is None:
        raise exceptions.PreventUpdate
    
    df = pd.DataFrame.from_dict(data)
    non_compliant_rows = set()  # To track rows with non-compliant data

    for col in columns:
        # Ensure the column has the 'type' key
        if 'type' not in col:
            continue

        if col['type'] == 'text':
            def is_convertible_to_numeric(val):
                if val is None:
                    return False
                try:
                    # Try to convert to float
                    float(val)
                    return True
                except (TypeError, ValueError):
                    return False
            
            # mask = df[col['name']].apply(lambda x: not isinstance(x, str) or is_convertible_to_numeric(x))
            mask = df[col['name']].apply(lambda x: x is not None and (not isinstance(x, str) or is_convertible_to_numeric(x)))



        elif col['type'] == 'numeric':
            def is_numeric(val):
                if val is None:
                    return False

                # If val is already numeric (float or int)
                if isinstance(val, (float, int)):
                    return True

                # If val is a string, attempt to convert to float after removing hyphens
                if isinstance(val, str):
                    try:
                        float(val.replace('-', ''))
                        return True
                    except (TypeError, ValueError):
                        return False
                return False

            # mask = df[col['name']].apply(lambda x: not is_numeric(x))
            mask = df[col['name']].apply(lambda x: x is not None and (not is_numeric(x)))

    
        elif col['type'] == 'datetime':
            # mask = df[col['name']].apply(lambda x: not isinstance(x, pd.Timestamp))
            mask = df[col['name']].apply(lambda x: x is not None and (not isinstance(x, pd.Timestamp)))
        else:
            continue

        # Find non-compliant indices and add them to the set
        non_compliant_indices = mask[mask].index.tolist()
        for idx in non_compliant_indices:
            non_compliant_rows.add(idx)  # Add row index to the set

    # Filter the dataframe to keep only rows with non-compliant data
    df_filtered = df[df.index.isin(non_compliant_rows)]
    # print(df_filtered)

    if df_filtered.empty:
        print("No datatype non-compliant data found")
        
        notification = dmc.Notification(
            title="No datatype non-complient data found!",
            id="simple-notify",
            color="yellow",
            action="show",
            message="",
            autoClose=3000,
            icon=DashIconify(icon="akar-icons:circle-alert")
        )
        return no_update, no_update, notification, no_update
    
    confirm_button = dmc.Button("Confirm Changes", id="btn-confirm-changes", style={"backgroundColor": "#12B886"}),
            
    # return df_filtered.to_dict('records'), []
    return df_filtered.to_dict('records'), df_filtered.index.tolist(), [], confirm_button


###################### CLEAN CELLS DATATYPE [CLEANING OPERATION] highlighting ######################
@callback(
    Output('editable-table', 'style_data_conditional', allow_duplicate=True),
    [Input('noncomplient-indices', 'data')],
    State('editable-table', 'columns'),
    State('editable-table', 'data'),
    prevent_initial_call=True
)
def style_noncompliant_dtype_cells(cache, columns, data):
    if not cache:
        raise exceptions.PreventUpdate

    df = pd.DataFrame.from_dict(data)
    style_data_conditional = []

    for col in columns:
        if 'type' not in col:
            continue

        if col['type'] == 'text':
            def is_convertible_to_numeric(val):
                if val is None:
                    return False
                try:
                    # Try to convert to float
                    float(val)
                    return True
                except (TypeError, ValueError):
                    return False
            
            # mask = df[col['name']].apply(lambda x: not isinstance(x, str) or is_convertible_to_numeric(x))
            mask = df[col['name']].apply(lambda x: x is not None and (not isinstance(x, str) or is_convertible_to_numeric(x)))
            color = '#fde047'  # Adjusted color for non-string data in a text column

        elif col['type'] == 'numeric':
            def is_numeric(val):
                if val is None:
                    return False

                if isinstance(val, (float, int)):
                    return True

                if isinstance(val, str):
                    try:
                        float(val.replace('-', ''))
                        return True
                    except (TypeError, ValueError):
                        return False
                return False

            # mask = df[col['name']].apply(lambda x: not is_numeric(x))
            mask = df[col['name']].apply(lambda x: x is not None and (not is_numeric(x)))
            color = '#6ee7b7'  # Adjusted color for non-numeric data in a numeric column
    
        elif col['type'] == 'datetime':
            # mask = df[col['name']].apply(lambda x: not isinstance(x, pd.Timestamp))
            mask = df[col['name']].apply(lambda x: x is not None and (not isinstance(x, pd.Timestamp)))
            color = '#c4b5fd'  # Adjusted color for non-datetime data in a datetime column
        else:
            continue

        non_compliant_indices = mask[mask].index.tolist()
        for idx in non_compliant_indices:
            style_data_conditional.append({
                'if': {'row_index': idx, 'column_id': col['name']},
                'backgroundColor': color,
            })

    return style_data_conditional


# ###################### CLEAN CELLS DATATYPE [CONFIRM BUTTON] (persist changes) ######################
@callback(
    Output('initial-table-data', 'data', allow_duplicate=True),
    Output('notifications-container', 'children', allow_duplicate=True),
    Input('btn-confirm-changes', 'n_clicks'),
    State('editable-table', 'data'),
    State('initial-table-data', 'data'),
    prevent_initial_call=True,
)
def clean_noncompliant_cells(n_clicks, current_data, original_data):
    if n_clicks is None:
        raise exceptions.PreventUpdate

    # Create DataFrames from the current and original data
    current_df = pd.DataFrame(current_data)
    original_df = pd.DataFrame(original_data)

    # Ensure 'ID' column is of the same data type in both DataFrames to match correctly
    current_df['ID'] = current_df['ID'].astype(original_df['ID'].dtype)

    # Update the original DataFrame based on the 'ID' column
    for _, row in current_df.iterrows():
        # Find the index of the row with the matching 'ID' in the original DataFrame
        row_id = row['ID']
        match_index = original_df[original_df['ID'] == row_id].index

        # If the matching row is found, update it
        if not match_index.empty:
            # Update only the columns that exist in the original DataFrame
            for idx in match_index:
                for col in original_df.columns:
                    original_df.at[idx, col] = row[col]
        # If the 'ID' is not found, append the new row with correct columns
        else:
            new_row = {col: row[col] for col in original_df.columns}
            original_df = original_df.append(new_row, ignore_index=True)

    # Reset the index to ensure it remains unique and sequential
    original_df.reset_index(drop=True, inplace=True)


    notification = dmc.Notification(
            title="Changes updated!",
            id="simple-notify",
            color="green",
            action="show",
            message="",
            autoClose=3000,
            icon=DashIconify(icon="akar-icons:circle-check")
        )

    return original_df.to_dict('records'), notification


###################### RESET TABLE ######################
@callback(
    Output('editable-table', 'data', allow_duplicate=True),
    Output('editable-table', 'style_data_conditional', allow_duplicate=True),
    Output('btn-confirm-changes-container', 'children', allow_duplicate=True),
    Input('btn-reset-table', 'n_clicks'),
    State('initial-table-data', 'data'),

    prevent_initial_call=True
)
def reset_table(n_clicks, initial_data):
    if n_clicks is None:
        raise exceptions.PreventUpdate

    return initial_data, [], []


if __name__ == '__main__':
    app.run(debug=True)
