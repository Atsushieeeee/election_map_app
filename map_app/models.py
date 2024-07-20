from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    polygon = models.JSONField()  # MySQLではJSONFieldを使用

    def __str__(self):
        return self.name
