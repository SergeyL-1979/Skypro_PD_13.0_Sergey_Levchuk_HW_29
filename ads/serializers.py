from rest_framework import serializers

from ads.models import Announcement
from users.models import Location


class AnnouncementListSerializer(serializers.ModelSerializer):
    # name = serializers.CharField()
    # location = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    class Meta:
        model = Announcement
        fields = "__all__"
        # fields = ["id", "text", "slug", "status", "created", "username", "skills"]


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    class Meta:
        model = Announcement
        fields = "__all__"


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    # Вывод ID, но поле не обязательное required=False
    id = serializers.IntegerField(required=False)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    class Meta:
        model = Announcement
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("skills")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        loc = Announcement.objects.create(**validated_data)

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            loc.locations.add(location_obj)

        loc.save()
        return loc


class AnnouncementUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateField(read_only=True)

    class Meta:
        model = Announcement
        fields = ["id", "text", "slug", "status", "created", "user", "skills"]

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("skills")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        loc = super().save()

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            location.locations.add(location_obj)

        loc.save()
        return loc


class AnnouncementDestroySerializer(serializers.ModelSerializer):
    model = Announcement
    fields = ["id", ]