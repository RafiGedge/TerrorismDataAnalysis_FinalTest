import urllib.parse
from flask import Blueprint, request, render_template
from queries.queries_service import get_regions
from maps.create_maps import create_map_for_active_groups

active_groups_bp = Blueprint('active_groups_bp', __name__)

options = ['All'] + get_regions()


@active_groups_bp.route('/active_groups', methods=['GET', 'POST'])
def active_groups():
    name = request.args.get('name')
    selected_item = 'All'
    if request.method == 'POST':
        selected_item = request.form.get('Options')
    url_map = f"map_for_active_groups?result={urllib.parse.quote(selected_item)}"
    return render_template('index.html', list_items=options, url_map=url_map,
                           action='active_groups', name=name if name else selected_item)


@active_groups_bp.route('/map_for_active_groups')
def map_for_active_groups():
    region = urllib.parse.unquote(request.args.get('result'))
    if region == 'All':
        region = None

    create_map_for_active_groups(region)
    return render_template("map.html")
