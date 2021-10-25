from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse

from django.conf import settings
from movies.models import Filmwork, RoleType


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    paginate_by = settings.API_MOVIES_PER_PAGE

    def _aggregate_person(self, role):
        return ArrayAgg('personrole__person_id__full_name', distinct=True, filter=Q(personrole__role=role))

    def get_queryset(self):
        qs = super(MoviesApiMixin, self).get_queryset()
        qs = qs.prefetch_related('genres', 'persons')
        qs = qs.values('id', 'title', 'description', 'creation_date', 'rating', 'type')
        qs = qs.annotate(
            genres=ArrayAgg('filmworkgenre__genre_id__name', distinct=True),
            actors=self._aggregate_person(RoleType.ACTOR),
            directors=self._aggregate_person(RoleType.DIRECTOR),
            writers=self._aggregate_person(RoleType.WRITER)
        )
        return qs

    def render_to_response(self, context):
        return JsonResponse(context)
