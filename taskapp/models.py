from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    
    UserChoices = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User')
    )
    user_type = models.CharField(max_length=20, choices=UserChoices, default='user')
    
    def __str__(self):
        return self.username
    
class Task(models.Model):
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    admin = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
   
    def __str__(self):
        return self.title
    
class TaskCompletionReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='completionreports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completion_reports')
    completion_date = models.DateTimeField(auto_now_add=True)
    worked_hours = models.PositiveIntegerField(null=True, blank=True)
    completion_report = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Report for {self.task.title} by {self.user.username}"
    
class DeletedTask(models.Model):
    org_id = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User,on_delete = models.CASCADE,related_name='deleted_tasks',null=True,blank=True)
    deleted_at = models.DateField(auto_now_add=True)