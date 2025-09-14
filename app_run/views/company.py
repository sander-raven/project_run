from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_run.helpers import get_company_details

__all__ = [
    'company_details',
]


@api_view(['GET'])
def company_details(request):
    return Response(get_company_details())
