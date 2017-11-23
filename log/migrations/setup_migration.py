from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations
from django.contrib.auth.models import Group, Permission

from log.models import Entry


def create_entries_permission(name, codename):
	content_type = ContentType.objects.get_for_model(Entry)
	permission = Permission.objects.create(
		codename=codename,
		name=name,
		content_type=content_type
	)
	return permission


def create_role_permissions():
	can_view_others_entries = create_entries_permission('Can view others entries', 'can_view_others_entries')
	can_view_entries_employee = create_entries_permission('Can view entries employee', 'can_view_entries_employee')
	can_view_entries_client = create_entries_permission('Can view entries client', 'can_view_entries_client')
	return can_view_entries_employee, can_view_others_entries, can_view_entries_client


def create_role_groups():
    pm = Group.objects.create(name='Project Manager')
    client = Group.objects.create(name='Client')
    employee = Group.objects.create(name='Employee')
    can_view_entries_employee, can_view_others_entries, can_view_entries_client = create_role_permissions()
    pm.permissions.add(can_view_others_entries, can_view_entries_employee, can_view_entries_client)
    entries_perm_codename = ['add_entry', 'change_entry', 'delete_entry']
    for perm in Permission.objects.filter(codename__in=entries_perm_codename):
        employee.permissions.add(perm)
        pm.permissions.add(perm)
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