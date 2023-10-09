import pandas as pd
from dash.exceptions import PreventUpdate


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

def cleanCell(cellValue, dataType, format = None):
    #todo add to logic
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