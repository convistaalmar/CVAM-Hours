from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations
from django.contrib.auth.models import Group, Permission

from log.models import Entry


def create_view_others_entries_permission():
	content_type = ContentType.objects.get_for_model(Entry)
	permission = Permission.objects.create(
		codename='can_view_others_entries',
		name='Can view others entries',
		content_type=content_type,
	)
	return permission


def create_view_entries_employee_permission():
	content_type = ContentType.objects.get_for_model(Entry)
	permission = Permission.objects.create(
		codename='can_view_entries_employee',
		name='Can view entries employee',
		content_type=content_type,
	)
	return permission


def create_role_permissions():
	can_view_others_entries = create_view_others_entries_permission()
	can_view_entries_employee = create_view_entries_employee_permission()
	return can_view_entries_employee, can_view_others_entries


def create_role_groups():
    pm = Group.objects.create(name='Project Manager')
    client = Group.objects.create(name='Client')
    can_view_entries_employee, can_view_others_entries = create_role_permissions()
    pm.permissions.add(can_view_others_entries)
    pm.permissions.add(can_view_entries_employee)
    client.permissions.add(can_view_others_entries)


def apply_migration(apps, schema_editor):
    create_role_groups()


def revert_migration(apps, schema_editor):
    Group.objects.filter(
        name__in=[
            u'Project Manager',
            u'Client'
        ]
    ).delete()
    Permission.objects.filter(
		name__in=[
			u'Can view entries employee',
			u'Can view others entries'
		]
	).delete()


class Migration(migrations.Migration):

    dependencies = [('log', '0002_auto_20171102_1802'),]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]