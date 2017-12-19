from django.contrib.admin import SimpleListFilter, RelatedFieldListFilter

from log.models import Project
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text


class FilterEntriesByProject(RelatedFieldListFilter):

	def get_lookup_choices(self, changelist):
		projects_available = list(
			set([project for project in changelist.queryset.values_list('project_id', flat=True)]))
		self.lookup_choices = Project.objects.filter(id__in=projects_available).values_list('id', 'name')

	def choices(self, changelist):
		self.get_lookup_choices(changelist)
		yield {
			'selected': self.lookup_val is None and not self.lookup_val_isnull,
			'query_string': changelist.get_query_string(
				{},
				[self.lookup_kwarg, self.lookup_kwarg_isnull]
			),
			'display': _('All'),
		}
		for pk_val, val in self.lookup_choices:
			yield {
				'selected': self.lookup_val == force_text(pk_val),
				'query_string': changelist.get_query_string({
					self.lookup_kwarg: pk_val,
				}, [self.lookup_kwarg_isnull]),
				'display': val,
			}
		if self.include_empty_choice:
			yield {
				'selected': bool(self.lookup_val_isnull),
				'query_string': changelist.get_query_string({
					self.lookup_kwarg_isnull: 'True',
				}, [self.lookup_kwarg]),
				'display': self.empty_value_display,
			}

	title = u'Project'

	parameter_name = 'project'
