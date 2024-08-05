from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.ImageField(upload_to='projects/')
    is_data_analysis = models.BooleanField(default=False)

    def __str__(self):
        return self.title