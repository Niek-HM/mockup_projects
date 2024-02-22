from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name