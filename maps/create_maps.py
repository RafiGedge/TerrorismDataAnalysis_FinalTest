import folium
from pathlib import Path
from queries.queries_part_a import get_victims_average, get_most_active_groups, get_correlation_victims_for_events
from queries.queries_part_b import get_unique_groups_by_area

path = Path(__file__).parent.parent / 'front' / 'templates' / 'map.html'


def create_empty_map():
    m = folium.Map(location=(21, 9), zoom_start=3)
    m.save(path)


def create_map_for_victims_average(region=None, limit_five: bool = False):
    data = get_victims_average(region, limit_five)
    coordinates_list = [i['location'] for i in data]
    m = folium.Map()
    for i in data:
        popup_content = f"""
                <div style="width:150px; font-size:14px;">
                    <h3>{i['region']}</h3>
                    <p>{i['average']}</p>
                </div>
                """
        folium.Marker(
            location=i['location'],
            popup=folium.Popup(popup_content, max_width=150),
        ).add_to(m)
    m.fit_bounds(coordinates_list, max_zoom=4)
    m.save(path)


def create_map_for_active_groups(region=None):
    data = get_most_active_groups(region)
    coordinates_list = [i['location'] for _, i in data.items()]
    m = folium.Map()
    for key, value in data.items():
        popup_content = f"""
                <div style="width:300px; font-size:14px;">
                    <h3>{key}</h3>
                    <ul>
                        {"".join(f"<li>{group_name}: {event_count}</li>"
                                 for group_name, event_count in value['groups'].items())}
                    </ul>
                </div>
                """
        folium.Marker(
            location=value['location'],
            popup=folium.Popup(popup_content, max_width=300),
        ).add_to(m)
    m.fit_bounds(coordinates_list, max_zoom=4)
    m.save(path)


def create_map_for_unique_groups(area):
    data = get_unique_groups_by_area(area)
    coordinates_list = [i['location'] for i in data]
    m = folium.Map()
    for i in data:
        popup_content = f"""
                <div style="width:100px; font-size:14px;">
                    <h3>{i['region']}</h3>
                    <p>{i['num_groups']}</p>
                </div>
                """
        folium.Marker(
            location=i['location'],
            popup=folium.Popup(popup_content, max_width=100),
        ).add_to(m)
    m.fit_bounds(coordinates_list, max_zoom=4)
    m.save(path)


def create_map_for_corr_victims_for_events(region=None):
    data = get_correlation_victims_for_events(region)
    coordinates_list = [i['location'] for i in data]
    m = folium.Map()
    for i in data:
        popup_content = f"""
                <div style="width:100px; font-size:14px;">
                    <h3>{i['region']}</h3>
                    <p>{i['correlation']}</p>
                </div>
                """
        folium.Marker(
            location=i['location'],
            popup=folium.Popup(popup_content, max_width=100),
        ).add_to(m)
    m.fit_bounds(coordinates_list, max_zoom=4)
    m.save(path)
