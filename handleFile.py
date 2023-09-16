import pandas as pd

def csvToDf(csvString):
    newDf = pd.read_csv(csvString)
    return newDf

def fillMissing(df, newValue):
    newDf = df.fillna(newValue)
    return newDf

def printStats(df):
    print("Missing per column")
    print(df.isnull().sum())
    print(f"Total Missing: {df.isnull().values.sum()}")

def fillRowIteratively(df, rowI):
    NaMapOfRow = df.iloc[rowI].isna()
    for columnName in NaMapOfRow.index:
        if (NaMapOfRow[columnName]):
            # temporarily, the prompt will say the row index (1  is first row)
            # todo, tell frontend where to edit and what the value is
            df.iloc[rowI][columnName] = input(f"give a value to fill in the missing data in row {rowI + 1} the column \"{columnName}\": ")

def fillColumnIteratively(df, columnName):
    #todo
    pass

# def formatDf(df):
#     newDf = df
#     return newDf

def dfToCsv(df, outputFile = None):
    if (not outputFile):
        return df.to_csv(index=False)
    df.to_csv(outputFile, index=False)

def dfToXml(df, outputFile = None):
    if (not outputFile):
        return df.to_xml(index=False)
    df.to_xml(outputFile, index=False)

def dfToHtml(df, outputFile = None):
    if (not outputFile):
        return df.to_html(index=False)
    df.to_html(outputFile, index=False)