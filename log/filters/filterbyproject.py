from .base_fieldfilter import BaseEntriesFilter

from log.models import Project, Entry
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text


class FilterEntriesByProject(BaseEntriesFilter):

    def get_lookup_choices(self, changelist):
        super(FilterEntriesByProject, self).get_lookup_choices(changelist)
        self.lookup_choices = Project.objects.filter(id__in=self.projects_available).values_list('id', 'name')

    title = u'Project'

    parameter_name = 'project'
