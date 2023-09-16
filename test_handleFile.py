from handleFile import *
# import pytest

#region CSV import dataframe, export dataframe, printstats
rawDf = csvToDf("./sampleData/missingData.csv")
print(rawDf)

csvString = dfToCsv(rawDf, "./output/rawData.csv")
print(csvString)

printStats(rawDf)
#endregion

#todo, xml and html implementation are also already built into pandas, consider just using them directly 

#region fill in missing values
filledDf = rawDf
for columnName in rawDf.columns:
    missingDataPlaceholder = input(f"give a value to fill in the missing data in the column \"{columnName}\": ")
    filledDf = filledDf.fillna(value={columnName : missingDataPlaceholder})
    print(filledDf)
dfToHtml(filledDf, "./output/filledDf.html")

printStats(filledDf)

filledDf = rawDf
for rowI in range(filledDf.shape[0]):
    fillRowIteratively(filledDf, rowI)
dfToHtml(filledDf, "./output/filledDfRowByRow.html")

printStats(filledDf)

#endregion
