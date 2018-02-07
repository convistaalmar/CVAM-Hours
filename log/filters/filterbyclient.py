from django.contrib.admin import SimpleListFilter
from .filterbyproject import FilterEntriesByProject
from log.models import Client, Entry, Project


class FilterEntriesByClient(FilterEntriesByProject):

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(FilterEntriesByClient, self).__init__(field, request, params, model, model_admin, field_path)
        self.title = 'client'

    def get_lookup_choices(self, changelist):
        qs = Entry.objects.all()
        if changelist.params:
            args = {}
            for key in changelist.params:
                if 'date' in key:
                    args[key] = changelist.params[key]
            qs = qs.filter(**args)
        projects_available = list(
            set([project for project in qs.values_list('project_id', flat=True)]))
        self.lookup_choices = Client.objects.filter(project__in=projects_available).values_list('id', 'name')

    title = u'Client'

    parameter_name = 'client'
