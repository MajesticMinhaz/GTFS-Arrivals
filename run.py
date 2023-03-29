from flask import jsonify
from core import create_app
from core import Config
from tasks import rq_app
from routes import update_data_blueprint
from routes import check_task_status_blueprint
from routes import stops_blueprint
from routes import clear_cache_blueprint


flask_app = create_app()
flask_app.config.from_object(Config)

rq_app.init_app(app=flask_app)

flask_app.app_context().push()
flask_app.register_blueprint(stops_blueprint, url_prefix='/stops')
flask_app.register_blueprint(update_data_blueprint, url_prefix='/update-data')
flask_app.register_blueprint(check_task_status_blueprint, url_prefix='/status')
flask_app.register_blueprint(clear_cache_blueprint, url_prefix='/clear-cache')


with open('.version', 'r') as version_number:
    version = version_number.read().strip()


@flask_app.route('/', methods=['GET'])
def root_page():
    data = {
        'version': version,
        'app': 'GTFS Stops'
    }
    return jsonify(data)
