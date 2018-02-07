from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from log.models import Employee


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_employee(sender, instance, created, **kwargs):
	if created:
		if not instance.groups.all():
			employee_group = Group.objects.get(name='Employee')
			instance.groups.add(employee_group)
		Employee.objects.create(user=instance)
		instance.is_staff = True
		instance.save()
	else:
		instance.employee.save()
