from django.db import models

class RoleUser(models.Model):
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    user_email = models.CharField("Email", max_length=200)

class Role(models.Model):
    name = models.CharField("Role", max_length=100)
    email = models.CharField("Email", max_length=200)
