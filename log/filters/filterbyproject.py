from django.contrib.admin import SimpleListFilter

from log.models import Project


class FilterEntriesByProject(SimpleListFilter):

    def lookups(self, request, model_admin):
        all_entries = Project.objects.all().distinct()
        if not request.user.is_superuser:
            all_entries = all_entries.filter(employee__user=request.user)

        response = [(entry.id, entry.name) for entry in all_entries]

        return response

    title = u'Project'

    parameter_name = 'project'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project=self.value())
        return queryset