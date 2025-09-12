"""Additional helper functions & classes"""
from enum import Enum
from django.conf import settings
from django.db.models import Q


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
