from django.contrib.admin import SimpleListFilter
from .filterbyproject import FilterEntriesByProject
from log.models import Client


class FilterEntriesByClient(FilterEntriesByProject):

    def get_lookup_choices(self, changelist):
        projects_available = list(
            set([project for project in changelist.queryset.values_list('project_id', flat=True)]))
        self.lookup_choices = Client.objects.filter(project__in=projects_available).values_list('id', 'name')

    title = u'Client'

    parameter_name = 'client'
