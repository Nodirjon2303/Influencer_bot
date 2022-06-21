from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Messages)
admin.site.register(Users)
admin.site.register(Sections)
admin.site.register(Category)
admin.site.register(ServiceCategory)
admin.site.register(UserTypeCategory)
admin.site.register(Services)

