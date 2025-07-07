from django.contrib import admin
from django_celery_results.models import TaskResult, GroupResult
from django.contrib import admin

# Register your models here.
admin.site.register(TaskResult)
admin.site.register(GroupResult)