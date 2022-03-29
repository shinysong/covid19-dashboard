from django.db import models


class test_api(models.Model):
    dmName = models.TextField()
    mainURL = models.URLField()
    dsCount = models.IntegerField()
