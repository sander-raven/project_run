"""Additional helper functions & classes"""
import math
from enum import Enum

from django.conf import settings
from django.db.models import Q
from geopy.distance import geodesic

from app_run.models import CollectibleItem, Position


class UserTypes(Enum):
    ATHLETE = 'athlete'
    COACH = 'coach'


def get_user_type_query(user_type_string: str) -> Q:
    """Get user type query for queryset filter"""
    if user_type_string == UserTypes.ATHLETE.value:
        return Q(is_staff=False)
    elif user_type_string == UserTypes.COACH.value:
        return Q(is_staff=True)
    else:
        return Q()


def get_company_details() -> dict:
    """Get company details"""
    return {
        'company_name': getattr(settings, 'COMPANY_NAME', ''),
        'slogan': getattr(settings, 'SLOGAN', ''),
        'contacts': getattr(settings, 'CONTACTS', ''),
    }


def assign_nearby_items_to_user(
        position: Position,
        radius: float = 100,
):
    """Assign nearby collectible items to user"""
    radius *= 1.1
    user = position.run.athlete
    user_latitude = position.latitude
    user_longitude = position.longitude

    one_degree_of_latitude_in_meters = 111_000
    lat_radius = radius / one_degree_of_latitude_in_meters
    lon_radius = radius / (
            one_degree_of_latitude_in_meters
            * math.cos(math.radians(user_latitude))
    )
    lat_min = user_latitude - lat_radius
    lat_max = user_latitude + lat_radius
    lon_min = user_longitude - lon_radius
    lon_max = user_longitude + lon_radius

    nearby_items = CollectibleItem.objects.filter(
        latitude__range=(lat_min, lat_max),
        longitude__range=(lon_min, lon_max),
    )
    user_position = (user_latitude, user_longitude)

    for item in nearby_items:
        item_position = (item.latitude, item.longitude)
        if geodesic(user_position, item_position).meters < radius:
            user.items.add(item)


def calculate_position_distance_and_speed(
        position: Position,
) -> tuple[float | None, float | None]:
    """Calculate position distance and speed"""
    distance = None
    speed = None
    current_point = (position.latitude, position.longitude)
    prev_position = position.run.positions.last()
    if prev_position:
        prev_point = (prev_position.latitude, prev_position.longitude)
        _distance = geodesic(current_point, prev_point)
        distance = round(prev_position.distance + _distance.kilometers, 2)
        if position.date_time is not None and prev_position.date_time is not None:
            _time = (position.date_time - prev_position.date_time).total_seconds()
            speed = round(_distance.meters / _time, 2)
    return distance, speed
