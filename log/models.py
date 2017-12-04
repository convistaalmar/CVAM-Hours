from datetime import datetime
from django.db import models
from django.conf import settings

class Entry(models.Model):
	
	employee = models.ForeignKey("Employee")	
	project = models.ForeignKey("Project")
	work_type = models.ForeignKey("WorkType")
	date = models.DateField(default=datetime.today)
	hours = models.TimeField(blank=True, help_text="You can also enter minutes.")
	message = models.CharField(max_length=255, help_text="Brief description of work done.<br>Add SVN revision or issue number if available.")

	billed = models.BooleanField(default=False)

	created = models.DateTimeField('Created at', auto_now_add=True)
	updated = models.DateTimeField('Updated at', auto_now=True)	
		
	def __str__(self):
		return "%s %s" % (self.date, self.hours)

	def hours_minutes(self):
		return self.hours.strftime("%H:%M")
	hours_minutes.short_description = 'Hours'	

	# Enable EmployeeFilterSpec
	project.employee_filter = True
	work_type.employee_filter = True

	class Meta:
		verbose_name_plural = "entries"
		ordering = ["date"]
		
class Client(models.Model):
	
	name = models.CharField(max_length=25)
		
	def __str__(self):
		return self.name
		
	class Meta:
		ordering = ["name"]		


class Project(models.Model):
	
	name = models.CharField(max_length=25)
	client = models.ForeignKey("Client")
		
	def __str__(self):
		return self.name
		
	class Meta:
		ordering = ["name"]			

class WorkType(models.Model):
	
	name = models.CharField(max_length=25)
		
	def __str__(self):
		return self.name
				
	class Meta:
		ordering = ["name"]			


class Employee(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
	project = models.ManyToManyField("Project")
	work_type = models.ManyToManyField("WorkType")
	
	def latest_entry(self):
		try:
			return self.entry_set.latest('updated')
		except: 
			return False
		
	def __str__(self):
		return self.user.get_full_name()
		
	class Meta:
		ordering = ["user__last_name"]				


