from django.db import models
import uuid
# Create your models here.


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    database_name = models.CharField(max_length=100)

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name