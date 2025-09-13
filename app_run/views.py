from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .helpers import get_company_details, get_user_type_query
from .models import AthleteInfo, Run
from .serializers import AthleteInfoSerializer, RunSerializer, UserSerializer

User = get_user_model()


@api_view(['GET'])
def company_details(request):
    return Response(get_company_details())


class RunPagination(PageNumberPagination):
    page_size_query_param = 'size'


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all().select_related('athlete')
    serializer_class = RunSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('athlete', 'status')
    ordering_fields = ('created_at',)
    pagination_class = RunPagination


def change_run_status(
        run_id: int,
        current_status: Run.Status,
        new_status: Run.Status,
) -> Response:
    """Change run status"""
    run = get_object_or_404(Run, pk=run_id)
    if run.status == current_status:
        run.status = new_status
        run.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StartRunView(APIView):
    def post(self, request, run_id: int):
        return change_run_status(
            run_id=run_id,
            current_status=Run.Status.INIT,
            new_status=Run.Status.IN_PROGRESS,
        )


class StopRunView(APIView):
    def post(self, request, run_id: int):
        return change_run_status(
            run_id=run_id,
            current_status=Run.Status.IN_PROGRESS,
            new_status=Run.Status.FINISHED,
        )


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


class AthleteInfoView(GenericAPIView):
    queryset = AthleteInfo.objects.all()
    serializer_class = AthleteInfoSerializer
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('user_id'))
        athlete_info, _ = AthleteInfo.objects.get_or_create(user=user)
        serializer = self.get_serializer(athlete_info)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('user_id'))
        defaults = dict()
        goals = request.POST.get('goals')
        if goals:
            defaults['goals'] = goals
        weight = request.POST.get('weight')
        if weight:
            try:
                weight = int(weight)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not (0 < weight < 900):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            defaults['weight'] = weight
        athlete_info, _ = AthleteInfo.objects.update_or_create(
            user=user,
            defaults=defaults,
        )
        serializer = self.get_serializer(athlete_info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
