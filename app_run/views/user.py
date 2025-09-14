from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from app_run.helpers import get_user_type_query
from app_run.models import Run
from app_run.serializers import UserSerializer

__all__ = [
    'UserViewSet',
]

User = get_user_model()


class UserPagination(PageNumberPagination):
    page_size_query_param = 'size'


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('first_name', 'last_name')
    ordering_fields = ('date_joined',)
    pagination_class = UserPagination

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get('type', None)
        query = get_user_type_query(user_type)
        qs = qs.filter(query).exclude(is_superuser=True)
        qs = qs.annotate(runs_finished=Count(
            'runs', filter=Q(runs__status=Run.Status.FINISHED)
        ))
        return qs
