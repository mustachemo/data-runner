import pandas as pd
import os
import io
import base64
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dashboard.utils.dataAnalysis import higlight_empty_nan_null_cells


def importFiles(prevData, files, fileNames):
    df = pd.DataFrame.from_dict(data=prevData)

    message = ""

    for index, file in enumerate(files):
        fileName = fileNames[index]
        _, content = file.split(",")
        _, ext = os.path.splitext(fileName)
        decodedStream = io.BytesIO(base64.b64decode(content))
        try:
            newDf = None
            match ext:
                case ".csv":
                    newDf = pd.read_csv(decodedStream)
                case ".xml":
                    newDf = pd.read_xml(decodedStream)
                case ".html":
                    newDf, *_ = pd.read_html(decodedStream)
                    # html may have multiple tables
                    # todo handle that case ^
                case ".xls" | ".xlsm" | ".xlsx":
                    newDf = pd.read_excel(decodedStream)
                    # todo pdf
                case _:
                    message += f"Unrecognized filetype '{fileName}'.\n"
            
            # Add an ID column to the new dataframe
            newDf['ID'] = range(1, len(newDf) + 1)

            # Ensure the ID column is the first column
            col_order = ['ID'] + [col for col in newDf.columns if col != 'ID']
            newDf = newDf[col_order]

            df = combineDf(df, newDf)
        except Exception as e:
            print(e)
            message += f"There was an error processing the file '{fileName}'.\n"

    data = df.to_dict("records")
    columns = [{"name": col, "id": col, "selectable": True, "renamable": True,
                "clearable": True, "hideable": True, "deletable": True} for col in df.columns]

    print(message)

    notification = dmc.Notification(
        title="Data loaded!",
        id="simple-notify",
        color="green",
        action="show",
        autoClose=3000,
        message=f'file name(s): {fileNames}',
        icon=DashIconify(icon="akar-icons:circle-check"),
    )

    # todo return message
    return data, columns, {'headers': True}, data, notification


def combineDf(prevDf, df):
    # todo prompt user to select specific columns to join on, may improve performance
    if (prevDf.empty):
        return df
    
   
    # Align the columns of both DataFrames
    df = df.reindex(columns=prevDf.columns)

    # Combine the DataFrames, prioritizing non-null values in prevDf
    combined_df = prevDf.combine_first(df)

    # Drop duplicates based on index
    combined_df = combined_df[~combined_df.index.duplicated(keep='first')]

    return combined_df


def exportFile(data, columns, fileType="csv"):
    message = ""
    df = pd.DataFrame.from_dict(data)
    columnNameMap = {col["id"]: col["name"] for col in columns}
    df = df.rename(columns=columnNameMap)
    match fileType:
        case "csv":
            return dict(content=df.to_csv(index=False), filename="data.csv")
        case "xml":
            return dict(content=df.to_xml(index=False), filename="data.xml")
        case "html":
            return dict(content=df.to_html(index=False), filename="data.html")
        # todo pdf xlsx
        case _:
            message += f"Unrecognized filetype '{fileType}'.\n"
            print(message)
            raise PreventUpdate
