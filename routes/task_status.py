from flask import Blueprint, jsonify
from rq.exceptions import NoSuchJobError
from rq.job import Job
from core import my_redis


# Create a Flask blueprint for checking the status of a task
check_task_status_blueprint = Blueprint('task-status', __name__)


@check_task_status_blueprint.route('/<string:task_id>', methods=['GET', 'POST'])
def task_status(task_id):
    """
    Endpoint for checking the status of a Celery task by task ID.
    """

    try:
        # Retrieve the RQ task result with the given ID
        task_result = Job.fetch(task_id, connection=my_redis)
        # Construct a response object with the task status and ID
    except NoSuchJobError:
        task_result = None

    if task_result:
        response = {
            'status': task_result.get_status(),
            'id': task_result.id,
            'task': task_result.func_name,
            'completed_at': task_result.ended_at,
            'started_at': task_result.enqueued_at
        }

    else:
        response = {
            'id': task_id,
            'status': 'No task found.'
        }

    # Return the response as a JSON object
    return jsonify(response)
