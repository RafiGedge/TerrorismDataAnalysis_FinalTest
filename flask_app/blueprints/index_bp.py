from flask import Blueprint, render_template, request, redirect, url_for
from maps.create_maps import create_empty_map

index_bp = Blueprint('index_bp', __name__)

option = ['הצגת ממוצע נפגעים לפי אזור', 'הצגת הקבוצות הפעילות ביותר לפי אזור', 'הצגת כמות הקבוצות השונות לפי אזור',
          'הצגת קורולציה בין נפגעים לפיגועים לפי אזור']
urls = ['victims_average_bp.victims_average', 'active_groups_bp.active_groups', 'unique_groups_bp.unique_groups',
        'corr_victims_for_events_bp.corr_victims_for_events']


@index_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_item = request.form.get('Options')
        return redirect(url_for(urls[option.index(selected_item)], name=selected_item))

    return render_template('index.html', list_items=option, url_map='empty_map', name='בחר שאילתא')


@index_bp.route('/empty_map')
def empty_map():
    create_empty_map()
    return render_template('map.html')
