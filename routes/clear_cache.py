from flask import Blueprint, jsonify
from core import my_redis
from core import Config
from datetime import datetime


# Create a Flask blueprint for checking the status of a task
clear_cache_blueprint = Blueprint('clear_cache', __name__)


@clear_cache_blueprint.route('/<string:passcode>', methods=['GET', 'POST'])
def clear_cache(passcode):
    if Config.UPDATE_DATA_PASSCODE == passcode:
        my_redis.flushdb()
        return jsonify({
            'msg': 'Redis Flushed',
            'datetime': datetime.utcnow()
        })
    else:
        return jsonify({
            'msg': 'Wrong Passcode!!'
        })
