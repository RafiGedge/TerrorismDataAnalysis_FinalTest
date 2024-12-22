import folium

from data.queries import get_average


def create_regions_map(region=None, limit_five: bool = False):
    data = get_average(region, limit_five)
    coordinates_list = [i['location'] for i in data]
    m = folium.Map()
    for i in data:
        folium.Marker(
            location=i['location'],
            popup=f"{i['region']}: {i['average']}",
        ).add_to(m)
    m.fit_bounds(coordinates_list, max_zoom=4)
    m.save("../front/templates/map.html")
