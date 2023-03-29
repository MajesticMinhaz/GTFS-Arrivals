def bulk_insert(model, session, data_list):
    """
    Bulk insert a list of data into a database table using SQLAlchemy ORM.

    Args:
        model: The SQLAlchemy ORM model representing the database table.
        session: The SQLAlchemy session object used to interact with the database.
        data_list: A list of dictionaries where each dictionary represents a row to be inserted.

    Returns:
        None

    Raises:
        Exception: If there is any error while inserting the data, an exception is raised.
    """
    try:
        for data in data_list:
            row = model(**data)
            session.add(row)
        session.commit()
    except Exception as e:
        # Log the error with a traceback and context information
        import traceback
        traceback.print_exc()
        session.rollback()
        raise Exception(f"Error while inserting data into {model.__tablename__} table: {e}")
