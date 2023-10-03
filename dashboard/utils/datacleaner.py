import base64
import io
import pandas as pd
from dash import html

class DataCleaner:

    @staticmethod
    def parse_contents(contents, filename, date):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                print(f'filename: {filename}')
                df = pd.read_excel(io.BytesIO(decoded))
                print(f'df: {df}')
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        print(f'df: {df}')
        return df