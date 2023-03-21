from rest_framework import serializers

from users.models import Location


class LocationListSerializer(serializers.ModelSerializer):
     class Meta:
        model = Location
        fields = "__all__"

class LocationDetailSerializer(serializers.ModelSerializer):
    # skills = serializers.SlugRelatedField(
    #     many=True, read_only=True, slug_field="name")
    class Meta:
        model = Location
        fields = "__all__"


class LocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class LocationDestroySerializer(serializers.ModelSerializer):
    model = Location
    fields = ["id", ]