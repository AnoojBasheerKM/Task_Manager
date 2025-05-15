from django.contrib import admin
from taskapp.models import User, Task, TaskCompletionReport

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(TaskCompletionReport)


