from rest_framework.generics import ListAPIView

from app_run.models import CollectibleItem
from app_run.serializers import CollectibleItemSerializer

__all__ = [
    'CollectibleItemListView',
]


class CollectibleItemListView(ListAPIView):
    queryset = CollectibleItem.objects.all()
    serializer_class = CollectibleItemSerializer
