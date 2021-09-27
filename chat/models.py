from django.db import models
from django.utils import timezone

# Create your models here.
class NegotiationsMessages(models.Model):
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    negotiation_id = models.IntegerField(default=1)
    owner_id = models.IntegerField()
    mType_id = models.IntegerField(default=1)
    class Meta:
        managed = False
        db_table = 'negotiations_messages'