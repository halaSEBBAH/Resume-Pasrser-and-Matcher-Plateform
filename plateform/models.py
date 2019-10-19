from django.db import models

# Create your models here.

class Cv(models.Model):
    CvRaw = models.CharField(max_length=1000000000)

    def __str__(self):
        return self.CvRaw

    class Meta:
        verbose_name_plural = "resumes"