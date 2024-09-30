from django.db import models
from django.conf import settings


class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Kitten(models.Model):
    COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('gray', 'Gray'),
        ('orange', 'Orange'),
        ('mixed', 'Mixed'),
    ]

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    age = models.PositiveIntegerField()  # возраст в месяцах
    description = models.TextField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='kittens')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rating(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.kitten} - {self.rating}'
