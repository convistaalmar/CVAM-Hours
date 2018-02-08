from .base_fieldfilter import BaseEntriesFilter
from log.models import Client


class FilterEntriesByClient(BaseEntriesFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(FilterEntriesByClient, self).__init__(field, request, params, model, model_admin, field_path)
        self.title = 'client'

    def get_lookup_choices(self, changelist):
        super(FilterEntriesByClient, self).get_lookup_choices(changelist)
        self.lookup_choices = Client.objects.filter(project__in=self.projects_available).values_list('id', 'name').distinct()

    title = u'Client'

    parameter_name = 'client'
