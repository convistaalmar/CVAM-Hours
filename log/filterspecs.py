# Based on http://djangosnippets.org/snippets/1051

from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class EmployeeFilterSpec(ChoicesFilterSpec):
	"""
	Filters using only the objects the employee is allowed to see.

	my_model_field.employee_filter = True
	"""

	def __init__(self, f, request, params, model, model_admin, field_path=None):
		super(EmployeeFilterSpec, self).__init__(f, request, params, model, model_admin, field_path)
		self.lookup_kwarg = '%s__exact' % f.name
		self.lookup_val = request.GET.get(self.lookup_kwarg, None)
		if request.user.is_superuser:
			self.lookup_choices = f.related.parent_model.objects.all().values_list('id','name')
		else:
			self.lookup_choices = getattr(request.user.employee, f.name).all().values_list('id','name')

		
	def choices(self, cl):
		yield {'selected': self.lookup_val is None,
			   'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
			   'display': _('All')}
		for k, v in self.lookup_choices:
			yield {'selected': smart_unicode(k) == self.lookup_val,
					'query_string': cl.get_query_string({self.lookup_kwarg: k}),
					'display': v}		

# Register the filter
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'employee_filter', False), EmployeeFilterSpec))