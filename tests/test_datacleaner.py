import dashboard.utils.datacleaner as DataCleaner
import os, pandas as pd

testsDir = os.path.dirname(__file__)

missingDataCombined = open(f"{testsDir}/testData/missingDataCombined.csv")
df = pd.read_csv(missingDataCombined)

# def test_cleanCell():
#     assert df == None