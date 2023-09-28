from dash import Dash, Input, Output, State, callback, callback_context, exceptions
import dash_bootstrap_components as dbc
import pandas as pd

from dashboard.utils.datacleaner import DataCleaner
from .layout import layout

dc = DataCleaner() # This is a class that contains the parse_contents method
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
def download_specific_file(_, fileType, dataTableData, current_columns):
    df = pd.DataFrame.from_dict(data=dataTableData)
    print(f'current_columns: {current_columns}')
    
    # Renaming columns based on current columns in DataTable
    renaming_dict = {col['id']: col['name'] for col in current_columns}
    df.rename(columns=renaming_dict, inplace=True)
    
    if fileType == 'csv':
        return dict(content=df.to_csv(index=False), filename="data.csv")
    if fileType == 'xml':
        return dict(content=df.to_xml(index=False), filename="data.xml")
    if fileType == 'html':
        return dict(content=df.to_html(index=False), filename="data.html")



@app.callback( # This is a callback that will highlight the selected columns
    Output('editable-table', 'style_data_conditional'),
    Input('editable-table', 'selected_columns')
    # Input('editable-table', 'selected_rows')
)
# def highlight_column_and_row(selected_columns, selected_rows):
def highlight_column(selected_columns):
    styles = []

    if selected_columns:
        styles.extend([{'if': {'column_id': col}, 'background_color': '#D2F3FF'} for col in selected_columns])

    # if selected_rows:
    #     styles.extend([{'if': {'row_index': row}, 'background_color': '#7FFF7F'} for row in selected_rows])

    return styles


@callback( # This is a callback that will upload the file and cache it
    Output('df-store', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def upload_file_and_cache(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is None:
        raise exceptions.PreventUpdate

    df = dc.parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
    return df.to_dict('records')


@callback( # This is a callback that will update the table with the data from the cache
    Output('editable-table', 'data'),
    Output('editable-table', 'columns'),
    Input('df-store', 'data')
)
def update_table(data):
    if data is None:
        raise exceptions.PreventUpdate

    df = pd.DataFrame.from_records(data)
    columns = [{'name': col, 'id': col, "selectable": True, "renamable": True,
                "clearable": True, "hideable": True, "deletable": True } for col in df.columns]
    return df.to_dict('records'), columns

if __name__ == '__main__':
    app.run(debug=True)
