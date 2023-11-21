from dash import html
import dash_mantine_components as dmc

definition_items = [
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("."), html.Span("Matches any character except a newline")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("^"), html.Span("Matches the start of the string")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("$"), html.Span("Matches the end of the string or just before the newline")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("*"), html.Span("Matches 0 or more repetitions of the preceding RE")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("+"), html.Span("Matches 1 or more repetitions of the preceding RE")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("?"), html.Span("Matches 0 or 1 repetitions of the preceding RE")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("{m,n}"), html.Span("Matches from m to n repetitions of the preceding RE")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={
                "display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"
            },
            children=[dmc.Kbd("[...]"), html.Span("Matches any character inside the square brackets")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={
                "display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"
            },
            children=[dmc.Kbd("[^...]"), html.Span("Matches any character not inside the square brackets")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("(?=...)"), html.Span("Matches if ... matches next, but doesn’t consume any of the string (lookahead assertion)")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("\\d"), html.Span("Matches any Unicode decimal digit")]
        ),
        xs=12, md=6
    ),
    dmc.Col(
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "start", "gap": "10px"},
            children=[dmc.Kbd("\\w"), html.Span("Matches Unicode word characters")]
        ),
        xs=12, md=6
    ),
]


# Create the header row
header_row = html.Tr([
    html.Th("Pattern"), 
    html.Th("Explanation"), 
    html.Th("Case")
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
        html.Tr([
        html.Td(dmc.Kbd(r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")), 
        html.Td("Matches a simple email address."), 
        html.Td(dmc.Highlight("'user@example.com'", highlight="user@example.com"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"https?://(?:www\.)?\w+\.\w+")), 
        html.Td("Matches HTTP and HTTPS URLs."), 
        html.Td(dmc.Highlight("'http://www.example.com'", highlight="http://www.example.com"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"\(\d{3}\)\s\d{3}-\d{4}")), 
        html.Td("Matches US phone number with area code in brackets."), 
        html.Td(dmc.Highlight("'(123) 456-7890'", highlight="(123) 456-7890"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"^\d{5}-\d{4}$")), 
        html.Td("Matches US ZIP code in 5-digit + 4 format."), 
        html.Td(dmc.Highlight("'12345-6789'", highlight="12345-6789"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"#[a-fA-F0-9]{6}")), 
        html.Td("Matches hexadecimal color codes."), 
        html.Td(dmc.Highlight("'#1a2b3c'", highlight="#1a2b3c"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"^[A-Z][a-z]+\s[A-Z][a-z]+$")), 
        html.Td("Matches people's names."), 
        html.Td(dmc.Highlight("'John Doe'", highlight="John Doe"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")), 
        html.Td("Matches email addresses (case-insensitive) with subdomains."), 
        html.Td(dmc.Highlight("'first.last@example.co.uk'", highlight="first.last@example.co.uk"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$")), 
        html.Td("Matches credit card numbers."), 
        html.Td(dmc.Highlight("'1234 5678 9012 3456'", highlight="1234 5678 9012 3456"))
    ]),
    html.Tr([
        html.Td(dmc.Kbd(r"\b\d{1,3}(,\d{3})*\b")), 
        html.Td("Matches numbers with commas for every thousand."), 
        html.Td(dmc.Highlight("'1,234,567'", highlight="1,234,567"))
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