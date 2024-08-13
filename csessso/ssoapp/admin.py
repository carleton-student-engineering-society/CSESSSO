from django.contrib import admin
from models import models

class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")

admin.site.register(models.Role, RoleAdmin)

class RoleUserAdmin(admin.ModelAdmin):
    list_display = ("role", "user_email")
    search_fields = ("role", "user_email")

admin.site.register(models.RoleUser, RoleUserAdmin)


