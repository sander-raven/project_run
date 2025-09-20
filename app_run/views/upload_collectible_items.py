import openpyxl
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_run.serializers import CollectibleItemSerializer

__all__ = [
    'upload_collectible_items',
]


@api_view(['POST'])
def upload_collectible_items(request):
    file = request.FILES.get('file')
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active
    headers = [cell.value.lower() for cell in sheet[1]]
    url_index = headers.index('url')
    headers[url_index] = 'picture'
    error_data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        serializer = CollectibleItemSerializer(data=row_data)
        if serializer.is_valid():
            serializer.save()
        else:
            error_data.append(list(row))
    return Response(data=error_data)
