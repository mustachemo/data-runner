import pandas as pd

def checkFileContents(file):
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    print(f'df.head(5): {df.head(5)}')
    print(f'df.shape: {df.shape}')
    print(f'df.size: {df.size}')
    print(f'df.ndim: {df.ndim}')
    print(f'df.columns: {df.columns}')
    print(f'df.info(): {df.info()}')
    print(f'df.describe(): {df.describe()}')