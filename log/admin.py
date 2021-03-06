from copy import copy
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.forms.fields import TimeField
from django.forms.widgets import TimeInput, Textarea
from django.utils.text import Truncator
from log.models import *
from log.filters.filterbyclient import FilterEntriesByClient
from log.filters.filterbyproject import FilterEntriesByProject


class EntryAdmin(admin.ModelAdmin):

	# Change form
	# Only show projects and worktypes for this user.
	# Default to the last project/worktype used.

	def mark_as_billed(modeladmin, request, queryset):
		queryset.update(billed=True)

	mark_as_billed.short_description = "Mark entries as billed"

	def mark_as_non_billed(modeladmin, request, queryset):
		queryset.update(billed=False)

	mark_as_non_billed.short_description = "Mark entries as non-billed"

	actions = ['mark_as_billed', 'mark_as_non_billed']

	def get_form(self, request, obj=None, **kwargs):
		selfie = copy(self)
		selfie.exclude = ['employee']
		if not request.user.is_superuser:
			selfie.exclude += ['billed']
		form = super(EntryAdmin, selfie).get_form(request, obj, **kwargs)
		return form

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		
		latest = request.user.employee.latest_entry()
			
		if db_field.name == 'project':
			kwargs['queryset'] = Project.objects.filter(employee=request.user.employee)
			if latest: kwargs['initial'] = latest.project
		if db_field.name == 'work_type':
			kwargs['queryset'] = WorkType.objects.filter(employee=request.user.employee)					
			if latest: kwargs['initial'] = latest.work_type

		return super(EntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


	# Simon Willison's row-level admin permissions 
	# http://djangosnippets.org/snippets/1054
	
	def get_queryset(self, request):
		qs = super(EntryAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		elif request.user.has_perm('log.can_view_others_entries'):
			return qs.filter(project__in=request.user.employee.project.all())
		else:
			return qs.filter(employee = request.user.employee)
	
	def save_model(self, request, obj, form, change):
		if not obj.pk: # So the admin can edit employee's hours
			obj.employee = request.user.employee
		obj.save()

	def has_change_permission(self, request, obj=None):
		if not obj:
			return True  # So they can see the change list page
		if (request.user.is_superuser or obj.employee == request.user.employee) or request.user.has_perm('log.change_entry'):
			return True
		else:
			return False

	def has_add_permission(self, request, obj=None):
		if not request.user.has_perm('log.add_entry'):
			self.list_display_links = (None,)
			return False
		if not obj:
			return True # So they can see the change list page
		else:
			return True

	def get_readonly_fields(self, request, obj=None):
		if obj:
			if not request.user.is_superuser and obj.employee != request.user.employee:
				return self.list_display + ['hours', 'message']
		return self.readonly_fields


	has_delete_permission = has_change_permission


	# Nice hours	
	def formfield_for_dbfield(self, db_field, **kwargs):
		field = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
		if db_field.name == 'hours':
			field = TimeField (
				input_formats=('%H','%H.%M','%H:%M'), 
				widget = TimeInput(format='%H:%M'),
				help_text=db_field.help_text,
			)
		elif db_field.name == 'message':
			field.widget = Textarea(attrs={'cols': 60, 'rows': 2})
		return field
	
	
	# Change list
	list_display = ['date', 'project', 'hours_minutes', 'message_text', 'work_type']	
	date_hierarchy = 'date'
	search_fields = ['message']
	list_filter = [('project', FilterEntriesByProject), 'work_type', ('project', FilterEntriesByClient)]

	
	def get_list_display(self, request):
		list_display = copy(self.list_display)
		if request.user.is_superuser or request.user.has_perm('log.can_view_entries_employee'):
			if 'employee' not in list_display: list_display += ['employee']
			if 'billed' not in list_display: list_display += ['billed']

		return list_display

	def get_actions(self, request):
		actions = super(EntryAdmin, self).get_actions(request)
		if not request.user.is_superuser:
			if 'mark_as_billed' in actions:
				del actions['mark_as_billed']
			if 'mark_as_non_billed' in actions:
				del actions['mark_as_non_billed']
		return actions

	def get_list_filter(self, request):
		list_filter = copy(self.list_filter)
		if request.user.is_superuser or request.user.has_perm('log.can_view_entries_employee'):
			if 'employee' not in list_filter: list_filter += ['employee']
			if 'billed' not in list_filter: list_filter += ['billed']

		return list_filter
	
	
	def changelist_view(self, request, extra_context=None):
		# Get a query set with same filters as the current change list
		from django.contrib.admin.views.main import ChangeList
		from datetime import timedelta
		cl = ChangeList(request, self.model, self.list_display, self.list_display_links, 
						self.list_filter, self.date_hierarchy, self.search_fields, 
						self.list_select_related, self.list_per_page, self.list_max_show_all, 
						self.list_editable, self)

		filtered_query_set = cl.get_queryset(request)
		hours = timedelta()
		for hour in [entry.hours for entry in filtered_query_set]:
			hours += timedelta(hours=hour.hour,minutes=hour.minute)
		
		seconds = hours.days * 86400 + hours.seconds
		hours, remainder = divmod(seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		total_hours = '%02d:%02d' % (hours, minutes)
							
		extra = {
			'total_hours': total_hours,
		}

		if extra_context: extra = extra.update(extra_context)
		
		return super(EntryAdmin, self).changelist_view(request, extra_context=extra)

		
	def message_text(self, obj): 
		return '<i>%s</i>' % Truncator(obj.message).words(40)
	message_text.allow_tags = True		


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Log admins	
admin.site.register(Entry, EntryAdmin)
admin.site.register(Project)
admin.site.register(Client)
admin.site.register(WorkType)
