import math


def get_centroid(coordinates: list[list]) -> tuple:
    x = 0
    y = 0
    z = 0
    try:
        for lat, lon in coordinates:
            latitude = math.radians(lat)
            longitude = math.radians(lon)
            x += math.cos(latitude) * math.cos(longitude)
            y += math.cos(latitude) * math.sin(longitude)
            z += math.sin(latitude)
    except TypeError:
        return None, None

    total = len(coordinates)
    x /= total
    y /= total
    z /= total

    central_longitude = math.degrees(math.atan2(y, x))
    central_square_root = math.sqrt(x * x + y * y)
    central_latitude = math.degrees(math.atan2(z, central_square_root))

    return central_latitude, central_longitude
