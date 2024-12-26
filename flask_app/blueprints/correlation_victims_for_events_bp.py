import urllib.parse
from flask import Blueprint, request, render_template
from maps.create_maps import create_map_for_corr_victims_for_events
from queries.queries_service import get_regions

corr_victims_for_events_bp = Blueprint('corr_victims_for_events_bp', __name__)

options = ['All'] + get_regions()


@corr_victims_for_events_bp.route('/corr_victims_for_events', methods=['GET', 'POST'])
def corr_victims_for_events():
    name = request.args.get('name')
    selected_item = 'All'
    if request.method == 'POST':
        selected_item = request.form.get('Options')
    url_map = f"map_for_corr_victims_for_events?result={urllib.parse.quote(selected_item)}"
    return render_template('index.html', list_items=options, url_map=url_map,
                           action='corr_victims_for_events', name=name if name else selected_item)


@corr_victims_for_events_bp.route('/map_for_corr_victims_for_events')
def map_for_corr_victims_for_events():
    region = urllib.parse.unquote(request.args.get('result'))
    if region == 'All':
        region = None

    create_map_for_corr_victims_for_events(region)
    return render_template("map.html")
