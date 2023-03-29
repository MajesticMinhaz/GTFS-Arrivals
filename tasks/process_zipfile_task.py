from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from more_itertools import chunked
from models import Calendar
from models import Trips
from models import Stops
from models import StopTimes
from models import Routes
from .rq_app import rq_app
from dependencies import parse_date
from dependencies import parse_time
from dependencies import parse_csv
from dependencies import parse_bool
from dependencies import bulk_insert
from dependencies import download_zipfile
from dependencies import extract_zipfile
from core import db


credentials = {
    'trips.txt': {
        'columns': ['route_id', 'service_id', 'trip_id', 'trip_headsign'],
        'mappers': {
            'service_id': int
        },
        'model': Trips
    },
    'calendar.txt': {
        'columns': ['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                    'start_date', 'end_date'],
        'mappers': {
            'service_id': int,
            'monday': parse_bool,
            'tuesday': parse_bool,
            'wednesday': parse_bool,
            'thursday': parse_bool,
            'friday': parse_bool,
            'saturday': parse_bool,
            'sunday': parse_bool,
            'start_date': parse_date,
            'end_date': parse_date
        },
        'model': Calendar
    },
    'routes.txt': {
        'columns': ['route_id', 'route_short_name', 'route_type'],
        'mappers': {
            'route_type': int
        },
        'model': Routes
    },
    'stops.txt': {
        'columns': ['stop_id', 'stop_name'],
        'model': Stops
    },
    'stop_times.txt': {
        'columns': ['trip_id', 'arrival_time', 'departure_time', 'stop_id'],
        'mappers': {
            'arrival_time': parse_time,
            'departure_time': parse_time
        },
        'model': StopTimes
    }
}


@rq_app.job(timeout=86400)
def process_zipfile_task(zipfile_url: str, selected_files: list, db_uri: str):
    # create SQLAlchemy engine and session
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Step 1: Download the zipfile
    zip_file = download_zipfile(file_url=zipfile_url)

    if not zip_file:
        return 'Bad ZipFile url found...'

    # Step 2: Extract the zipfile
    extracted_zip_info = extract_zipfile(zip_file, *selected_files)

    # Step 3: Delete the zip_file variable to reuse memory
    del zip_file

    for filename, content in extracted_zip_info:
        cred = credentials.get(filename)

        if not cred:
            continue

        csv_data = parse_csv(file=content, columns=cred.get('columns'), mappers=cred.get('mappers'))

        chunked_data = chunked(csv_data, 1000)

        session.execute(cred.get('model').__table__.delete())
        session.commit()

        if filename == 'stop_times.txt':
            session.execute(db.text(f"ALTER SEQUENCE {cred.get('model').__tablename__}_id_seq RESTART WITH 1"))
            session.commit()

        for data in chunked_data:
            bulk_insert(
                model=cred.get('model'),
                session=session,
                data_list=data
            )
    return 'File processed successfully'
