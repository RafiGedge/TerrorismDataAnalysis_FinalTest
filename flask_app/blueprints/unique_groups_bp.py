from flask import Blueprint, request, render_template
from maps.create_maps import create_map_for_unique_groups

unique_groups_bp = Blueprint('unique_groups_bp', __name__)

options = ['Region', 'Country']


@unique_groups_bp.route('/unique_groups', methods=['GET', 'POST'])
def unique_groups():
    name = request.args.get('name')
    selected_item = 'Region'
    if request.method == 'POST':
        selected_item = request.form.get('Options')
    url_map = f'/map_for_unique_groups?result={selected_item}'
    return render_template('index.html', list_items=options, url_map=url_map,
                           action='unique_groups', name=name if name else selected_item)


@unique_groups_bp.route('/map_for_unique_groups')
def map_for_unique_groups():
    area = request.args.get('result')
    create_map_for_unique_groups(area)
    return render_template('map.html')
