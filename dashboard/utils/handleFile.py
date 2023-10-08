import pandas as pd, os, io, base64
from dash.exceptions import PreventUpdate

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

            df = combineDf(df, newDf)
        except Exception as e:
            print(e)
            message += f"There was an error processing the file '{fileName}'.\n"

    data = df.to_dict("records")
    columns = [{"name": col, "id": col, "selectable": True, "renamable": True,
                "clearable": True, "hideable": True, "deletable": True} for col in df.columns]
    
    print(message)

    # todo return message
    return data, columns

def combineDf(prevDf, df):
    # todo prompt user to select specific columns to join on, may improve performance
    if (prevDf.empty):
        return df
    newDf = pd.concat([prevDf, df], join="inner", ignore_index=True)
    newDf = newDf.drop_duplicates()
    # drop_duplicates sometimes works, seems to depends on the datatypes of the combined df columns
    # todo resolve bug ^
    return newDf

def exportFile(data, columns, fileType = "csv"):
    if (data == None or columns == None):
        raise PreventUpdate
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