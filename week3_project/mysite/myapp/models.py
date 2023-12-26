from django.db import models

class BoanNews(models.Model):
    title = models.CharField(primary_key=True, max_length=255)
    url = models.TextField(blank=True, null=True)
    writer = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boannews'