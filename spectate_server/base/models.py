from django.db import models


# Create your models here.
class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    # active = ActiveManager()

    class Meta:
        abstract = True


class Sport(BaseModel):
    name = models.CharField(max_length=50, null=True)
    slug = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Event(BaseModel):
    SPORT_CHOICES = [
        ('preplay', 'Preplay'),
        ('inplay', 'Inplay'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('started', 'Started'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]
    name = models.CharField(max_length=50, null=True)
    slug = models.CharField(max_length=50, null=True)
    event_type = models.CharField(max_length=50, null=True, choices=SPORT_CHOICES)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, null=True, choices=STATUS_CHOICES)
    scheduled_start = models.DateTimeField(null=True)
    actual_start = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Selection(BaseModel):
    OUTCOME_CHOICES = [
        ('unsettled', 'Unsettled'),
        ('void', 'Void'),
        ('lose', 'Lose'),
        ('win', 'Win'),
    ]
    name = models.CharField(max_length=100, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(null=True)
    outcome = models.CharField(max_length=50, null=True, choices=OUTCOME_CHOICES)

    def __str__(self):
        return self.name
