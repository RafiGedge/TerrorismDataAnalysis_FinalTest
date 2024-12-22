import urllib.parse

from flask import Flask, request, render_template

from data.front_queries import get_regions
from maps.create_map_by_region import create_regions_map

app = Flask(__name__, template_folder='../front/templates', static_folder='../front/static')


@app.route('/', methods=['GET', 'POST'])
def index():
    selected_item = 'All'
    if request.method == 'POST':
        selected_item = request.form.get('mySelect')
    url_map = f"map_by_region?result={urllib.parse.quote(selected_item)}"
    return render_template('index.html', list_items=(['All', 'Top5'] + get_regions()), url_map=url_map)


@app.route('/map_by_region')
def map_by_region():
    params = {'region': None, 'limit_five': False}
    result = urllib.parse.unquote(request.args.get('result'))

    if result == 'Top5':
        params['limit_five'] = True
    elif result not in ('All', 'None'):
        params['region'] = result

    create_regions_map(**params)
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)
