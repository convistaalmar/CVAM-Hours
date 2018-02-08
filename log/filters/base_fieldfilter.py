from django.contrib.admin import RelatedFieldListFilter
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from log.models import Entry


class BaseEntriesFilter(RelatedFieldListFilter):
	def __init__(self, field, request, params, model, model_admin, field_path):
		super(BaseEntriesFilter, self).__init__(field, request, params, model, model_admin, field_path)
		self.projects = request.user.employee.project.all()
		self.projects_available = []

	def get_lookup_choices(self, changelist):
		qs = Entry.objects.filter(project__in=self.projects)
		if changelist.params:
			args = {}
			for key in changelist.params:
				if 'date' in key:
					args[key] = changelist.params[key]
			qs = qs.filter(**args)
		self.projects_available = list(
			set([project for project in qs.values_list('project_id', flat=True)]))

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