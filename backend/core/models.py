from django.db import models
from django.core.validators import URLValidator
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')



class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Company(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Domain(models.Model):
    company = models.ForeignKey(Company, related_name='domains', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_link = models.URLField(validators=[URLValidator()], blank=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    mandays = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.mandays:
            self.mandays = sum(task.mandays for task in self.tasks.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        (0, 'Not Started'),
        (1, 'In Progress'),
        (2, 'Paused'),
        (3, 'Completed')
    ]

    domain = models.ForeignKey(Domain, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)
    parent_task = models.ForeignKey('self', related_name='subtasks', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_link = models.URLField(validators=[URLValidator()], blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    mandays = models.FloatField(default=0)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def save(self, *args, **kwargs):
        if not self.mandays:
            self.mandays = sum(subtask.mandays for subtask in self.subtasks.all())
        
        latest_action = self.actions.order_by('-start_date').first()
        if latest_action:
            self.status = latest_action.status

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Action(models.Model):
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'In Progress'),
        (2, 'Blocked'),
        (3, 'Completed')
    ]

    task = models.ForeignKey(Task, related_name='actions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    action = models.ForeignKey(Action, related_name='discussion', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    document_link = models.URLField(validators=[URLValidator()], blank=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.date}"
