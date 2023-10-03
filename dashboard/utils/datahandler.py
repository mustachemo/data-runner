import pandas as pd
from dash import exceptions
import dash as dcc
from dashboard.utils.datacleaner import DataCleaner as dc


class DataHandler:

    def __init__(self, df):
        self.df = df

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
        
    # def highlight_column_and_row(selected_columns, selected_rows):
    def highlight_column(self, selected_columns):
        styles = []

        if selected_columns:
            styles.extend([{'if': {'column_id': col}, 'background_color': '#D2F3FF'} for col in selected_columns])

        # if selected_rows:
        #     styles.extend([{'if': {'row_index': row}, 'background_color': '#7FFF7F'} for row in selected_rows])

        return styles
    
    def upload_file_and_cache(self, list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is None:
            raise exceptions.PreventUpdate

        self.df = dc.parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
        return self.df.to_dict('records')
    
    def update_table(self, data):
        if data is None:
            raise exceptions.PreventUpdate

        self.df = pd.DataFrame.from_records(data)
        columns = [{'name': col, 'id': col, "selectable": True, "renamable": True,
                    "clearable": True, "hideable": True, "deletable": True } for col in self.df.columns]
        return self.df.to_dict('records'), columns