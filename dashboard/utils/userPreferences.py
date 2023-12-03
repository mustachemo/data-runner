from dash import html, dcc
import dash_mantine_components as dmc
import json
from dashboard.utils.parameters import definition_items, regex_table


def extract_dropdown_values(children):
    """
    Helper function to extract dropdown values from the modal's children.
    """
    dropdown_values = []

    for child in children:  # children is a list of Divs
        # if child is a dict and child's type is Div
        if isinstance(child, dict) and child.get('type') == 'Div':
            for inner_child in child['props']['children']:  # inner_child is a Div
                if inner_child['type'] == 'Dropdown':  # inner_child is a Dropdown
                    # inner_child's value is the dropdown value
                    dropdown_values.append(inner_child['props']['value'])

    return dropdown_values

def extract_input_values(children):
    input_values = []

    for child in children:
        if isinstance(child, dict) and child.get('type') == 'Div':
            for inner_child in child['props']['children']:
                if inner_child['type'] == 'TextInput':
                    input_values.append(inner_child['props']['value'])

    return input_values

def populate_datatype_selection(opened, columns):
    data_type_options = ["text", "numeric",  "datetime", "any"]
    children = []

    for col_details in columns:
        col_name = col_details['name']
        if col_name == 'ID':
            continue
        dropdown_value = col_details.get('type', 'any')

        dropdown = dcc.Dropdown(
            id={'type': 'datatype-dropdown', 'index': col_name},
            options=[{'label': dt, 'value': dt}
                     for dt in data_type_options],
            value=dropdown_value,
            placeholder="Select data type",
            style={'width': '9rem'}
        )

        children.append(
            html.Div(
                [html.Label(col_name), dropdown],
                style={"display": "flex", "justifyContent": "space-between",
                       "alignItems": "center", "padding": "0.5rem", "borderBottom": "1px solid #000"}
            )
        )

    return children

def populate_format_selection(opened, columns, formatting_options):

    formatting_options = json.loads(formatting_options) if formatting_options else None

    children = []
    children.append(create_regex_instructional_area())
    children.append(dmc.Space(h=20))

    for col_details in columns:
        col_name = col_details['name']
        if col_name == 'ID':
            continue

        # Retrieve the format from the stored formatting if it exists, otherwise set to None
        placeholder_value = formatting_options.get(col_name, None) if formatting_options else None

        input_text = dmc.TextInput(
            id={'type': 'format-input', 'index': col_name},
            value=placeholder_value,
            placeholder="Enter format",
            style={'width': '20rem'}
        )

        
        children.append(
            html.Div(
                [html.Label(col_name), input_text],
                style={"display": "flex", "justifyContent": "space-between",
                       "alignItems": "center", "padding": "0.5rem", "borderBottom": "1px solid #000"}
            )
        )

    return children

def create_regex_instructional_area():
    return dmc.Alert(
          children=[
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-around",
                    "alignItems": "center",
                    "marginBottom": "1rem"
                },
                children=[
                    dmc.Title(order=4, children="Understanding Regular Expressions"),
                    html.A(
                        "Learn More",
                        href="https://docs.python.org/3/library/re.html",
                        target="_blank",
                        style={
                            "textDecoration": "none",
                            "color": "inherit",
                            "padding": "10px 20px",
                            "border": "1px solid",
                            "borderRadius": "4px",
                        }
                    )
                ]
            ),
            dmc.AccordionMultiple(children=[
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl("Common Definitions"),
                        dmc.AccordionPanel(
                            dmc.Grid(
                                children=definition_items,
                                style={"margin": "0 auto"}
                            ),
                            style={"textAlign": "center"}
                        )
                    ],
                    value="definitions",
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl("Common Examples"),
                        dmc.AccordionPanel(
                            dmc.List(
                                children=regex_table
                        )
                        )
                    ],
                    value="examples",
                )
            ]),
        ],
        style={"maxWidth": "70rem", "margin": "0 auto"}
    )


