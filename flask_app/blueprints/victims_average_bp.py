import urllib.parse
from flask import Blueprint, request, render_template
from queries.queries_service import get_regions
from maps.create_maps import create_map_for_victims_average

victims_average_bp = Blueprint('victims_average_bp', __name__)

options = ['All', 'Top5'] + get_regions()


@victims_average_bp.route('/victims_average', methods=['GET', 'POST'])
def victims_average():
    name = request.args.get('name')
    selected_item = 'All'
    if request.method == 'POST':
        selected_item = request.form.get('Options')
    url_map = f"map_for_victims_average?result={urllib.parse.quote(selected_item)}"
    return render_template('index.html', list_items=options, url_map=url_map,
                           action='victims_average', name=name if name else selected_item)


@victims_average_bp.route('/map_for_victims_average')
def map_for_victims_average():
    params = {'region': None, 'limit_five': False}
    result = urllib.parse.unquote(request.args.get('result'))

    if result == 'Top5':
        params['limit_five'] = True
    elif result not in ('All', 'None'):
        params['region'] = result

    create_map_for_victims_average(**params)
    return render_template("map.html")
