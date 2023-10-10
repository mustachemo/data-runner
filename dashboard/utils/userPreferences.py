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
