from django.db import models
from django.utils import timezone
# Create your models here.


class Members(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default=None)
    rank = models.CharField(max_length=20, default=None)
    date = models.DateField(default=timezone.now)
    on_activate = models.BooleanField()

    def __str__(self):
        return self.name


class MeetingInfo(models.Model):
    date = models.DateField()
    count = models.IntegerField()
    theme = models.CharField(max_length=100)

    empty_strings_allowed = True
    attendance = models.ManyToManyField(
        Members, blank=True, related_name="attendance")
    best_table_topic_speaker = models.ForeignKey(
        Members, related_name="best_table_topic_speaker",
        blank=True, on_delete=models.CASCADE)
    best_prepared_speaker = models.ForeignKey(
        Members,  related_name="best_prepared_speaker",
        blank=True, on_delete=models.CASCADE)
    best_evaluator_speaker = models.ForeignKey(
        Members,  related_name="best_evaluator_speaker",
        blank=True, on_delete=models.CASCADE)

    toastmaster_of_day = models.ForeignKey(
        Members,  related_name="toastmaster_of_day",
        blank=True, on_delete=models.CASCADE)
    table_topic_master = models.ForeignKey(
        Members,  related_name="table_topic_master",
        blank=True, on_delete=models.CASCADE)
    general_evaluator = models.ForeignKey(
        Members,  related_name="general_evaluator",
        blank=True, on_delete=models.CASCADE)
    ah_counter = models.ForeignKey(
        Members,  related_name="ah_counter",
        blank=True, on_delete=models.CASCADE)
    grammarian = models.ForeignKey(
        Members,  related_name="grammarian",
        blank=True, on_delete=models.CASCADE)
    timer = models.ForeignKey(
        Members,  related_name="timer", blank=True, on_delete=models.CASCADE)

    individual_evaluator = models.ManyToManyField(
        Members, blank=True, related_name="individual_evaluator")

    def __str__(self):
        return str(self.date) + "   #" + str(self.count) + "_" + self.theme


class Speakers(models.Model):
    role_takers = models.ForeignKey(MeetingInfo, on_delete=models.CASCADE)
    project_rank = models.CharField(max_length=10)
    speaker_name = models.ForeignKey(
        Members,  related_name="speaker_name",
        blank=True, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=100)

    def __str__(self):
        return self.name


