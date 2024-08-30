from django.contrib import admin
from .models import Job,JobCategory,JobApply
# Register your models here.




class JobAdmin(admin.ModelAdmin):
    list_display = ['company','title','salary','status']

admin.site.register(Job,JobAdmin)
admin.site.register(JobCategory)
admin.site.register(JobApply)
