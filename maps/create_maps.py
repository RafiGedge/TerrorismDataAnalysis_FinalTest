import folium

from data.queries.queries_part_a import get_victims_average, get_most_active_groups


def create_map_for_victims_average(region=None, limit_five: bool = False):
    data = get_victims_average(region, limit_five)
    coordinates_list = [i['location'] for i in data]
    m = folium.Map()
    for i in data:
        folium.Marker(
            location=i['location'],
            popup=f"{i['region']}: {i['average']}",
        ).add_to(m)
    m.fit_bounds(coordinates_list, max_zoom=4)
    m.save("../front/templates/map_for_victims_average.html")


def create_map_for_active_groups(region=None):
    data = get_most_active_groups(region)
    coordinates_list = [i['location'] for _, i in data.items()]
    m = folium.Map()
    for key, value in data.items():
        folium.Marker(
            location=value['location'],
            popup=f"{key}: {[(k, v) for k, v in value['groups'].items()]}",
        ).add_to(m)
    m.fit_bounds(coordinates_list, max_zoom=4)
    m.save("../front/templates/map_for_active_groups.html")
