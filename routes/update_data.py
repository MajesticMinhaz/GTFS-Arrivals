from flask import Blueprint, jsonify, request
from tasks import process_zipfile_task
from core import my_redis
from dependencies import should_execute_process_zip_task
from core import Config


# Create a Flask blueprint for updating a dataset
update_data_blueprint = Blueprint('update-data', __name__)


@update_data_blueprint.route('/<string:passcode>/', methods=['GET', 'POST'])
def update_data(passcode):
    file_url = request.args.get('url')

    if not file_url:
        file_url = 'https://data.bus-data.dft.gov.uk/timetable/download/gtfs-file/all/'

    selected_files = ['calendar.txt', 'stops.txt', 'routes.txt', 'trips.txt', 'stop_times.txt']

    if passcode == Config.UPDATE_DATA_PASSCODE and file_url:

        # Check if the update dataset task should be executed
        if should_execute_process_zip_task(redis=my_redis):

            # Start the process_zipfile_task Celery task with the given credential
            result = process_zipfile_task.queue(file_url, selected_files, Config.SQLALCHEMY_DATABASE_URI)

            # Construct a response object with the task ID and URL to check the task status
            data = {
                'task_id': result.id,
                'check_status': f'/status/{result.id}'
            }
        else:
            # Construct a response object indicating that the task has already been executed today
            data = {
                'msg': 'Task already executed today, skipping...'
            }
    else:
        data = {
            'msg': 'Something went wrong',
            'zipfile_url': file_url
        }

    return jsonify(data)
