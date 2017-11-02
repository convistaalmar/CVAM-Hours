from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from log.models import Employee


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_employee(sender, instance, created, **kwargs):
	if created:
	    Employee.objects.create(user=instance)
	else:
        instance.employee.save()
