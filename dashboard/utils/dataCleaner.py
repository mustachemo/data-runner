import pandas as pd
from dash.exceptions import PreventUpdate
from dash import no_update
import re
import json
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def show_noncomplient_empty_data(columns, data):
        
    df = pd.DataFrame.from_dict(data)
    non_compliant_rows = set()  # To track rows with non-compliant data

    for col in columns:
        # Find non-compliant indices and add them to the set
        non_compliant_indices = df[col['name']].apply(lambda x: pd.isna(x))
        non_compliant_rows.update(non_compliant_indices[non_compliant_indices].index.tolist())

    # Filter the dataframe to keep only rows with non-compliant data
    df_filtered = df.loc[list(non_compliant_rows)]

    if df_filtered.empty:
        notification = dmc.Notification(
            title="No empty/corrupt data found!",
            id="simple-notify",
            color="yellow",
            action="show",
            message="",
            autoClose=3000,
            icon=DashIconify(icon="akar-icons:circle-alert")
        )
        return no_update, no_update, notification, no_update
    
    confirm_button = dmc.Button("Confirm Changes", id="btn-confirm-changes", style={"backgroundColor": "#12B886"})

    return df_filtered.to_dict('records'), df_filtered.index.tolist(), [], confirm_button


def style_noncompliant_empty_cells(columns, data):
     
    df = pd.DataFrame.from_dict(data)
    style_data_conditional = []

    for col in columns:
        # Find non-compliant indices
        non_compliant_indices = df[col['name']].apply(pd.isna)
        non_compliant_rows = non_compliant_indices[non_compliant_indices].index.tolist()

        for idx in non_compliant_rows:
            style_data_conditional.append({
                'if': {'row_index': idx, 'column_id': col['name']},
                'backgroundColor': '#f87171',  # Red background to highlight non-compliant cells
            })

    return style_data_conditional


def show_noncompliant_format_data(formatting_store_data, columns, data):

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
        return no_update, no_update, notification, no_update
    
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
        notification = dmc.Notification(
            title="No format non-complient data found!",
            id="simple-notify",
            color="yellow",
            action="show",
            message="",
            autoClose=3000,
            icon=DashIconify(icon="akar-icons:circle-alert")
        )
        return no_update, no_update, notification, no_update
    
    confirm_button = dmc.Button("Confirm Changes", id="btn-confirm-changes", style={"backgroundColor": "#12B886"})
            
    return df_filtered.to_dict('records'), df_filtered.index.tolist(), [], confirm_button


def style_noncompliant_format_cells(columns, data, formatting_store_data):
    
    if formatting_store_data is None:
        return no_update

    # Load the stored formatting options
    formatting_options = json.loads(formatting_store_data)
    df = pd.DataFrame.from_dict(data)
    style_data_conditional = []

    for col in columns:
        col_name = col['name']
        # Ensure the column has a formatting pattern stored
        if col_name in formatting_options:
            pattern = formatting_options[col_name]
            regex = re.compile(pattern)

            # Find non-compliant indices and add them to the set
            non_compliant_indices = df[col_name].apply(lambda x: not regex.match(str(x)) if x else False)
            non_compliant_rows = non_compliant_indices[non_compliant_indices].index.tolist()

            for idx in non_compliant_rows:
                style_data_conditional.append({
                    'if': {'row_index': idx, 'column_id': col['name']},
                    'backgroundColor': '#93c5fd',
                })

    return style_data_conditional


def show_noncomplient_dtype_data(columns, data):
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

def style_noncompliant_dtype_cells(columns, data):
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








def cleanDataAuto(data, columns, preferences):
    if (data == None or columns == None):
        print("Nothing to clean")
        raise PreventUpdate
    message = ""
    changedCells = []
    emptyCells = []
    needsAttention = []

    df = pd.DataFrame.from_dict(data)

    for column in columns:
        columnId = column["id"]
        columnData = df[columnId]
        dataType = None
        if (columnId in preferences):
            dataType = preferences[columnId]
        else:
            dataType = preferences["*"]
        for rowIndex, cellValue in enumerate(columnData):
            if (cellValue is None):
                needsAttention.append((columnId, rowIndex))
                emptyCells.append((columnId, rowIndex))
            else:
                newCellValue, isCleaned = cleanCell(cellValue, dataType)
                if (not isCleaned):
                    needsAttention.append((columnId, rowIndex))
                elif (newCellValue != cellValue):
                    df[columnId].iloc[rowIndex] = newCellValue
                    changedCells.append((columnId, rowIndex))

    newData = df.to_dict("records")
    return newData, message, changedCells, emptyCells, needsAttention


def cleanCell(cellValue, dataType, format=None):
    # todo add to logic
    # returns newCellValue, isCleaned
    try:
        match dataType:
            case "int":
                return int(cellValue), True
            case _:
                return cellValue, False
    except Exception as e:
        print("unable to convert", e)
        return cellValue, False


def remove_duplicate_rows(data, n_clicks):
    df = pd.DataFrame.from_dict(data)
    df.drop_duplicates(inplace=True)
    return df.to_dict('records')
