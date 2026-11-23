import pytest


def format_data_for_display(people_data):
    """Format each person's title, given name, and family name for display."""
    return [
        f"{person['title']} {person['given_name']} {person['family_name']}"
        for person in people_data
    ]


@pytest.fixture
def example_people_data():
    return [
        {"given_name": "Alice", "family_name": "Smith", "title": "Dr."},
        {"given_name": "Bob", "family_name": "Johnson", "title": "Mr."},
        {"given_name": "Charlie", "family_name": "Brown", "title": "Ms."},
    ]


def test_format_data_for_display(example_people_data):
    formatted_data = format_data_for_display(example_people_data)
    expected_output = ["Dr. Alice Smith", "Mr. Bob Johnson", "Ms. Charlie Brown"]
    assert formatted_data == expected_output
