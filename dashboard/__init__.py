from dash import Dash, Input, Output, State, callback, callback_context, exceptions, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

from dashboard.utils.datacleaner import DataCleaner as dc
from .layout import layout

# This is the data handler object (see dashboard/utils/datahandler.py)
dc = dc()
df = pd.DataFrame()
# This is the main app object
app = Dash(__name__)
# Improves load time by not loading all callbacks at once. 5-10% improvement
app.config.suppress_callback_exceptions = True

app.layout = layout


###################### UPLOAD FILE ######################
@callback(
    Output('editable-table', 'data'),
    Output('editable-table', 'columns'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def upload_file(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is None:
        raise exceptions.PreventUpdate

    df = dc.parse_contents(
        list_of_contents[0], list_of_names[0], list_of_dates[0])
    columns = [{'name': col, 'id': col, "selectable": True, "renamable": True,
                "clearable": True, "hideable": True, "deletable": True} for col in df.columns]

    return df.to_dict('records'), columns


###################### DOWNLOAD FILE ######################
@callback(
    Output("download-file", "data"),
    [Input("btn-download", "n_clicks")],
    [State('framework-select', 'value'),
     State('editable-table', 'data'),
     State('editable-table', 'columns')],
    prevent_initial_call=True,
)
def download_specific_files(_, fileType, dataTableData, current_columns):
    df = pd.DataFrame.from_dict(data=dataTableData)

    # Renaming columns based on current columns in DataTable
    renaming_dict = {col['id']: col['name'] for col in current_columns}
    df.rename(columns=renaming_dict, inplace=True)

    if fileType == 'csv':
        return dict(content=df.to_csv(index=False), filename="data.csv")
    if fileType == 'xml':
        return dict(content=df.to_xml(index=False), filename="data.xml")
    if fileType == 'html':
        return dict(content=df.to_html(index=False), filename="data.html")


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
