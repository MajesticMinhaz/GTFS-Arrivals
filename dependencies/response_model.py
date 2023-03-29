from typing import List


def response_model_creator(dataset: List[dict]) -> dict:
    """
    Creates a response model for a given dataset of rows.

    Args:
        dataset: A list of dictionaries containing trip, service, and time information.

    Returns:
        A dictionary containing stop_name and stops information.
    """
    # Initialize the result dictionary with empty values for stop_name and stops
    result = {
        "stop_name": None,
        "stops": []
    }

    # Iterate through each row in the dataset
    for row in dataset:

        # If stop_name has not been set yet, set it to the value in the current row
        if not result['stop_name']:
            result['stop_name'] = row['stop_name']

        # Create a dictionary to store arrival information for the current row
        arrival = {
            "route_name": row["route_name"],
            "destination": row['destination'],
            "arrival": row["arrival"],
            "departure": row["departure"]
        }

        # Add the arrival dictionary to the result's "stops" list
        result["stops"].append(arrival)

    # Return the completed result dictionary
    return result
