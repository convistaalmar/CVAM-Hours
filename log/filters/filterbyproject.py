from django.contrib.admin import SimpleListFilter

from log.models import Project


class FilterEntriesByProject(SimpleListFilter):

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            all_entries = Project.objects.all().distinct()
        else:
            all_entries = Project.objects.filter(employee__user=request.user).distinct()

        response = [(entry.id, entry.name) for entry in all_entries]

        return response

    title = u'Client'

    parameter_name = 'client'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project=self.value())
        return queryset