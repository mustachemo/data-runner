from dash import Dash, Input, Output, State, callback, callback_context, exceptions
import dash_bootstrap_components as dbc
import pandas as pd

from dashboard.utils.datacleaner import DataCleaner as dc
from .layout import layout

# This is the data handler object (see dashboard/utils/datahandler.py)
dc = dc()
df = pd.DataFrame()
# This is the main app object
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
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

    df.df = dc.parse_contents(
        list_of_contents[0], list_of_names[0], list_of_dates[0])
    columns = [{'name': col, 'id': col, "selectable": True, "renamable": True,
                "clearable": True, "hideable": True, "deletable": True} for col in df.df.columns]

    return df.df.to_dict('records'), columns


###################### DOWNLOAD FILE ######################
@callback(  # This is a callback that will download the file
    Output("download-file", "data"),
    [Input("btn-download", "n_clicks")],
    [State('framework-select', 'value'),
     State('editable-table', 'data'),
     State('editable-table', 'columns')],
    prevent_initial_call=True,
)
def download_specific_files(self, _, fileType, dataTableData, current_columns):
    self.df = pd.DataFrame.from_dict(data=dataTableData)

    # Renaming columns based on current columns in DataTable
    renaming_dict = {col['id']: col['name'] for col in current_columns}
    self.df.rename(columns=renaming_dict, inplace=True)

    if fileType == 'csv':
        return dict(content=self.df.to_csv(index=False), filename="data.csv")
    if fileType == 'xml':
        return dict(content=self.df.to_xml(index=False), filename="data.xml")
    if fileType == 'html':
        return dict(content=self.df.to_html(index=False), filename="data.html")


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
