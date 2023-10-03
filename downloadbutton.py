import dash_mantine_components as dmc
from dash import Dash, html, Output, Input, callback

app = Dash(__name__)

data = [["csv", "csv"], ["xsls", "xsls"], ["pdf", "pdf"], ["html", "html"], ["xml", "xml"]]

app.layout = html.Div(
    [
        dmc.Button("Download", style={"backgroundColor": "#0C7FDA"}),
        dmc.RadioGroup(
            [dmc.Radio(l, value=k) for k, l in data],
            id="radiogroup-simple",
            value="react",
            size="sm",
            mt=10,
        ),      
    ]
)

if __name__ == "__main__":
    app.run_server()