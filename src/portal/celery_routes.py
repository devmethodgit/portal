from flask import Blueprint, jsonify

from config import ConfigApp

celery_bp = Blueprint("celery", __name__)


@celery_bp.get("/test")
def test_page():
    return jsonify(message="Hello, DIT!"), ConfigApp.ResponseStatusCode.OK


@celery_bp.get("/update")
def update():
    from celdery.tasks import update_data

    update_data.delay()
    return jsonify(message="Updating..."), ConfigApp.ResponseStatusCode.OK
