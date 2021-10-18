from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies_admin.movies.models import Filmwork


class Movies(BaseListView):
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        qs = super(Movies, self).get_queryset().values()
        return qs

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }
        return context


class MoviesDetailApi(BaseDetailView):
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        id = self.kwargs[self.pk_url_kwarg]
        qs = super(MoviesDetailApi, self).get_queryset()
        qs = qs.prefetch_related('genres', 'persons')
        qs = qs.filter(id=id).values('id', 'title', 'description', 'creation_date', 'rating', 'type')
        qs = qs.annotate(
            genres=ArrayAgg('filmworkgenre__genre_id__name', distinct=True),
            actors=ArrayAgg('personrole__person_id__full_name', distinct=True, filter=Q(personrole__role='actor')),
            directors=ArrayAgg('personrole__person_id__full_name', distinct=True,
                               filter=Q(personrole__role='director')),
            writers=ArrayAgg('personrole__person_id__full_name', distinct=True, filter=Q(personrole__role='writer')),

        )
        return qs

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)

    def get_context_data(self, **kwargs):
        context = list(self.get_queryset())

        return context
