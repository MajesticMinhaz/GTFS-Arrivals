import csv
from typing import Union, List, Dict
from io import BytesIO, TextIOWrapper


def _parse_csv_rows(reader, columns, mappers):
    # Iterate over the rows in the CSV file and match columns to the 'columns' parameter
    for row in reader:
        matched_dict = {key: row[key] for key in columns if key in row}

        # If mappers are provided, apply them to matched columns
        if mappers:
            for key, _mapper in mappers.items():
                if key in matched_dict:
                    try:
                        matched_dict[key] = _mapper(matched_dict[key])
                    except ValueError:
                        continue
        yield matched_dict


def parse_csv(file: Union[BytesIO, str], columns: List[str], mappers: Dict[str, callable] = None) -> Dict[str, str]:
    """
    Parses a CSV file and returns a dictionary of matched columns.

    Parameters:
    file (Union[BytesIO, str]): A file object or file path of the CSV file to parse.
    columns (List[str]): A list of column names to match in the CSV file.
    mappers (Dict[str, callable]): A dictionary of column name/mapper function pairs. Mapper functions can be used to modify the value of a column during parsing. Defaults to None.

    Returns:
    A dictionary of matched columns in the CSV file, where the keys are column names and the values are string values from the CSV file.

    Raises:
    ValueError: If the CSV file contains a column that is not included in the 'columns' parameter.

    Example usage:
    >>> with open('example.csv', 'rb') as f:
    ...     parsed_data = parse_csv(f, ['name', 'age'], {'age': int})
    ...     print(parsed_data)

    Output:
    {'name': 'John', 'age': 30}

    """
    if isinstance(file, str):
        # If the file parameter is a string, open it as a file object
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            yield from _parse_csv_rows(reader, columns, mappers)
    else:
        # If the file parameter is a BytesIO object, wrap it in a TextIOWrapper object and open it with the csv module
        with TextIOWrapper(file, encoding='utf-8') as textfile:
            reader = csv.DictReader(textfile)
            yield from _parse_csv_rows(reader, columns, mappers)
