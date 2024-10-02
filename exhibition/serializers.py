from rest_framework import serializers
from .models import Breed, Kitten, Rating


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = '__all__'


class KittenSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    breed = serializers.ReadOnlyField(source='breed.name')

    class Meta:
        model = Kitten
        fields = ['pk', 'name', 'color', 'age', 'description', 'breed', 'user']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Rating
        fields = '__all__'
