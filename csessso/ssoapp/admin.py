from django.contrib import admin
from models import models

class RoleAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Role, RoleAdmin)

class RoleUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.RoleUser, RoleUserAdmin)


