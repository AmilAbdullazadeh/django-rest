from post.models import Post
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from favourite.models import Favourite


class FavouriteListCreateAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"

        def validate(self, attrs):
            queryset = Favourite.objects.filter(post=attrs["post"], user=attrs["user"])
            if queryset.exists():
                raise serializers.ValidationError("Bu post onsuzda elave edildi. Tekrar elave edile bilmez")
            return attrs


class FavouriteAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ("content",)
