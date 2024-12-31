from flask import Blueprint, jsonify
from load_data.load_primary_data import load_data

load_data_bp = Blueprint('load_data_bp', __name__)


@load_data_bp.route('/insert_data')
def insert_data():
    load_data()
    return jsonify('success', 'data inserted successfully'), 201
