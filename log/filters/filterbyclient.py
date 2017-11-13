from django.contrib.admin import SimpleListFilter

from log.models import Client, Entry


class FilterEntriesByClient(SimpleListFilter):

    def lookups(self, request, model_admin):
        all_entries = Client.objects.filter(project__employee__user=request.user).distinct()

        response = [(entry.id, entry.name) for entry in all_entries]

        return response

    title = u'Client'

    parameter_name = 'client'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__client=self.value())
        return queryset