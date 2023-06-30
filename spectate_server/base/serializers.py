from rest_framework import serializers

from base.models import Event, Selection


class GetSportSerializer(serializers.Serializer):
    class Filter(serializers.Serializer):
        totalEvent = serializers.IntegerField(allow_null=True, default=0)
        name = serializers.CharField(allow_blank=True, default='')
        slug = serializers.CharField(allow_blank=True, default='')
        active = serializers.BooleanField(allow_null=True, default=False)

    filter = Filter()


class GetEventSerializer(serializers.Serializer):
    class Filter(serializers.Serializer):
        totalSelection = serializers.IntegerField(allow_null=True, default=0)
        name = serializers.CharField(allow_blank=True, default='')
        scheduled_date = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S%z'])
        actual_date = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S%z'])
        slug = serializers.CharField(allow_blank=True, default='')
        active = serializers.BooleanField(allow_null=True, default=False)
        event_type = serializers.ChoiceField(choices=Event.SPORT_CHOICES, allow_blank=True)
        status = serializers.ChoiceField(choices=Event.STATUS_CHOICES, allow_blank=True)

    filter = Filter()


class GetSelectionSerializer(serializers.Serializer):
    class Filter(serializers.Serializer):
        name = serializers.CharField(allow_blank=True, default='')
        outcome = serializers.ChoiceField(allow_blank=True, choices=Selection.OUTCOME_CHOICES)
        active = serializers.BooleanField(allow_null=True, default=True)
        price = serializers.DictField(child=serializers.FloatField(default=0))

    filter = Filter()


class CreateSportSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(max_length=100)
    active = serializers.BooleanField()


class CreateEventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(max_length=100)
    active = serializers.BooleanField()
    event_type = serializers.ChoiceField(choices=Event.SPORT_CHOICES)
    sport_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Event.STATUS_CHOICES)
    scheduled_start = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    actual_start = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], allow_null=True)


class CreateSelectionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    event_id = serializers.IntegerField()
    price = serializers.FloatField()
    active = serializers.BooleanField()
    outcome = serializers.ChoiceField(choices=Selection.OUTCOME_CHOICES)


class UpdateSportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=100)
    active = serializers.BooleanField()


class UpdateEventSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=100)
    active = serializers.BooleanField()
    event_type = serializers.ChoiceField(choices=Event.SPORT_CHOICES)
    status = serializers.ChoiceField(choices=Event.STATUS_CHOICES)
    scheduled_start = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    actual_start = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], allow_null=True)


class UpdateSelectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    active = serializers.BooleanField()
    outcome = serializers.ChoiceField(choices=Selection.OUTCOME_CHOICES)
