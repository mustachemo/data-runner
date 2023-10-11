from dash import html
import dash_core_components as dcc


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


def populate_datatype_selection(opened, columns):
    data_type_options = ["text", "numeric",  "datetime", "any"]
    children = []

    for col_details in columns:
        col_name = col_details['name']
        dropdown_value = col_details.get('type', None)

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
