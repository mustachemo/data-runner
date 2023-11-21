from dash import html, dcc
import dash_mantine_components as dmc

definition_items = [
    dmc.ListItem([dmc.Kbd("\\d"), " - Digit (0-9)"]),
    dmc.ListItem([dmc.Kbd("\\w"), " - Alphanumeric (a-z, A-Z, 0-9)"]),
    dmc.ListItem([dmc.Kbd("\\s"), " - Whitespace (space, tab)"]),
    dmc.ListItem([dmc.Kbd("^"), " - Start of string"]),
    dmc.ListItem([dmc.Kbd("$"), " - End of string"]),
    dmc.ListItem([dmc.Kbd("[]"), " - Character set"]),
    dmc.ListItem([dmc.Kbd("[^]"), " - Negated set"]),
    dmc.ListItem([dmc.Kbd("()"), " - Group"]),
    dmc.ListItem([dmc.Kbd("|"), " - Or"]),
    dmc.ListItem([dmc.Kbd("?"), " - Zero or one"]),
    dmc.ListItem([dmc.Kbd("*"), " - Zero or more"]),
    dmc.ListItem([dmc.Kbd("+"), " - One or more"]),
    dmc.ListItem([dmc.Kbd("{n}"), " - Exactly n"]),
    dmc.ListItem([dmc.Kbd("{n,}"), " - n or more"]),
    dmc.ListItem([dmc.Kbd("{n,m}"), " - Between n and m"]),
    dmc.ListItem([dmc.Kbd("."), " - Any character (except newline)"]),
    dmc.ListItem([dmc.Kbd("\\"), " - Escape special character"]),
    dmc.ListItem([dmc.Kbd("\\A"), " - Start of string"]),
    dmc.ListItem([dmc.Kbd("\\b"), " - Word boundary"]),
    dmc.ListItem([dmc.Kbd("\\B"), " - Non-word boundary"]),
]

# Create the header row
header_row = html.Tr([
    html.Th("Pattern"), 
    html.Th("Explanation"), 
    html.Th("Example")
])

# Create the data rows
data_rows = [
    html.Tr([
        html.Td(dmc.Kbd("ab(cd|ef)")), 
        html.Td("Matches 'abcd' or 'abef'."), 
        html.Td([dmc.Highlight("'abcdxyz', ", highlight="abcd"), dmc.Highlight("'abefxyz'", highlight="abef")])
    ]),
    html.Tr([
        html.Td(dmc.Kbd("(a|b)c")), 
        html.Td("Matches 'ac' or 'bc'."), 
        html.Td([dmc.Highlight("'acxyz', ", highlight="ac"), dmc.Highlight("'bcxyz'", highlight="bc")])
    ]),
]

# Create the table component
regex_table = dmc.Table(
    striped=True,
    highlightOnHover=True,
    children=[
        html.Thead(header_row),
        html.Tbody(data_rows)
    ]
)


example_items = [
   dmc.ListItem([
        dmc.Kbd("ab(cd|ef)"), 
        " - Matches 'abcd' or 'abef'. Example: ", 
        dmc.Highlight("'abcd' in 'abcdxyz', 'abef' in 'abefxyz'", highlight="abcd|abef")
    ]),
    dmc.ListItem([
        dmc.Kbd("(a|b)c"), 
        " - Matches 'ac' or 'bc'. Example: ", 
        dmc.Highlight("'ac' in 'acxyz', 'bc' in 'bcxyz'", highlight="ac|bc")
    ]),
    dmc.ListItem([
        dmc.Kbd("\\d{2,4}"), 
        " - Matches 2 to 4 digits. Example: ", 
        dmc.Highlight("'12' in '1234', '123' in '1234', '1234' in '1234'", highlight="12|123|1234")
    ]),
    dmc.ListItem([
        dmc.Kbd("a\\d+b"), 
        " - Matches 'a' followed by one or more digits, then 'b'. Example: ", 
        dmc.Highlight("'a123b' in 'a123bxyz'", highlight="a123b")
    ]),
    dmc.ListItem([
        dmc.Kbd("\\b\\w+\\b"), 
        " - Matches whole words. Example: ", 
        dmc.Highlight("'hello' in 'hello world'", highlight="hello")
    ]),
    dmc.ListItem([
        dmc.Kbd("[A-Z]{3}"), 
        " - Matches any three uppercase letters. Example: ", 
        dmc.Highlight("'ABC' in 'ABCdef'", highlight="ABC")
    ]),
    dmc.ListItem([
        dmc.Kbd("\\w+@\\w+\\.com"), 
        " - Matches email addresses ending in '.com'. Example: ", 
        dmc.Highlight("'user@example.com' in 'user@example.com'", highlight="user@example.com")
    ]),
    dmc.ListItem([
        dmc.Kbd("https?://\\w+\\.\\w+"), 
        " - Matches HTTP and HTTPS URLs. Example: ", 
        dmc.Highlight("'http://example.com' and 'https://example.com'", highlight="http://example.com|https://example.com")
    ]),
    dmc.ListItem([
        dmc.Kbd("\\d+\\.\\d{2}"), 
        " - Matches a number with two decimal places. Example: ", 
        dmc.Highlight("'123.45' in 'The price is 123.45 dollars'", highlight="123.45")
    ]),
    dmc.ListItem([
        dmc.Kbd("\\[\\w+\\]"), 
        " - Matches text within brackets. Example: ", 
        dmc.Highlight("'[tag]' in 'This is a [tag] in text'", highlight="[tag]")
    ]),
]



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

def populate_format_selection(opened, columns):
    children = []

    for col_details in columns:
        col_name = col_details['name']
        dropdown_value = col_details.get('format', None)

        input_text = dcc.Input(
            id={'type': 'format-input', 'index': col_name},
            value=dropdown_value,
            placeholder="Enter format",
            style={'width': '9rem'}
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
            dmc.Title(order=4, children="Understanding Regular Expressions", style={"textAlign": "center"}),
            dmc.Divider(my="sm"),
            dmc.AccordionMultiple(children=[
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl("Common Definitions"),
                        dmc.AccordionPanel(
                            dmc.List(
                                children=definition_items
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
            html.A(
                "Learn More",
                href="https://docs.python.org/3/library/re.html",
                target="_blank",
                style={
                    "textDecoration": "none",
                    "color": "inherit",
                    "padding": "10px 20px",
                    "border": "1px solid",
                    "display": "inline-block",
                    "marginTop": "10px",
                    "borderRadius": "4px"
                }
            )
        ],
        style={"maxWidth": 800, "margin": "0 auto"}
    )


