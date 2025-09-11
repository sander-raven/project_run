from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers import get_company_details


@api_view(['GET'])
def company_details(request):
    return Response(get_company_details())
