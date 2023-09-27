from dash import Dash, Input, Output, State, callback, callback_context, exceptions
import dash_bootstrap_components as dbc
import pandas as pd

from dashboard.utils.datacleaner import DataCleaner
from .layout import layout

dc = DataCleaner()
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True # Improves load time by not loading all callbacks at once. 5-10% improvement

app.layout = layout

@callback(
    Output("download-file", "data"),
    State('radio-items', 'value'),
    State('editable-table', 'data'),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def download_specific_file(fileType, dataTableData, _):
    df = pd.DataFrame.from_dict(data=dataTableData)
    if fileType == 'csv':
        return dict(content=df.to_csv(index=False), filename="data.csv")
    if fileType == 'xml':
        return dict(content=df.to_xml(index=False), filename="data.xml")
    if fileType == 'html':
        return dict(content=df.to_html(index=False), filename="data.html")



@app.callback(
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


@callback(
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


@callback(
    Output('editable-table', 'data'),
    Output('editable-table', 'columns'),
    Input('df-store', 'data')
)
def update_table(data):
    if data is None:
        raise exceptions.PreventUpdate

    df = pd.DataFrame.from_records(data)
    columns = [{'name': col, 'id': col, "selectable": True} for col in df.columns]
    return df.to_dict('records'), columns

if __name__ == '__main__':
    app.run(debug=True)
