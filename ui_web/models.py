from django.db import models
from django.utils import timezone

# Create your models here.


class MeetingInfo(models.Model):
    data = models.DateField()
    count = models.CharField(max_length=10)
    theme = models.CharField(max_length=100)
    attendance = models.TextField()
    best_table_topic_speaker = models.CharField(max_length=100)
    best_prepared_speaker = models.CharField(max_length=100)
    best_evaluator_speaker = models.CharField(max_length=100)

    def __unicode__(self):
        return self.theme


class RoleTakers(models.Model):
    meeting_info = models.ForeignKey(MeetingInfo, on_delete=models.CASCADE)
    toastmaster_of_day = models.CharField(max_length=100)
    table_topic_master = models.CharField(max_length=100)
    general_evaluator = models.CharField(max_length=100)
    ah_counter = models.CharField(max_length=100, default=None)
    grammarian = models.CharField(max_length=100, default=None)
    timer = models.CharField(max_length=100, default=None)
    individual_evaluator = models.CharField(max_length=100, default=None)

    def __unicode__(self):
        return self.toastmaster_of_day


class Speakers(models.Model):
    role_takers = models.ForeignKey(RoleTakers, on_delete=models.CASCADE)
    rank = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Members(models.Model):
    name = models.CharField(max_length=100)
    data_time = models.CharField(max_length=100, default=timezone.now)
    on_activate = models.BooleanField()

    def __unicode__(self):
        return self.name
