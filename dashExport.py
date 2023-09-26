from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(['csv', 'xml', 'html'], 'csv', id='dropdown'),
    dcc.Download(id="download-text"),
])

df = pd.read_csv("./sampleData/missingData.csv")

@callback(
    Output("download-text", "data"),
    Input('dropdown', 'value'),
    prevent_initial_call=True,
)
def func(fileType, n_clicks):
    if n_clicks == 0:
        return
    if fileType == 'csv':
        n_clicks = 0
        return dict(content=df.to_csv(index=False), filename="data.csv")
    if fileType == 'xml':
        return dict(content=df.to_xml(index=False), filename="data.xml")
    if fileType == 'html':
        return dict(content=df.to_html(index=False), filename="data.html")


if __name__ == "__main__":
    app.run(debug=True)
