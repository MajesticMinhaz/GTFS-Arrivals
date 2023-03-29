from .rq_app import rq_app


@rq_app.exception_handler
def send_alert_to_ops(job, *exc_info):
    # call other code to send alert to OPs team
    print(f"Exception occurred while processing job {job.id}: {exc_info}")
