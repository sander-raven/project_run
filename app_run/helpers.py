"""Additional helper functions"""
from django.conf import settings


def get_company_details() -> dict:
    """Get company details"""
    return {
        'company_name': getattr(settings, 'COMPANY_NAME', ''),
        'slogan': getattr(settings, 'SLOGAN', ''),
        'contacts': getattr(settings, 'CONTACTS', ''),
    }
