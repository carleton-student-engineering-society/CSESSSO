from django.db import models

class RoleUser(models.Model):
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    user_email = models.CharField("Email", max_length=200)

    def __str__(self) -> str:
        return f"{self.role} - {self.user_email}"

class Role(models.Model):
    name = models.CharField("Role", max_length=100)
    email = models.CharField("Email", max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"
