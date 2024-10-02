from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'порода'
        verbose_name_plural = 'породы'
        ordering = ('pk',)


class Kitten(models.Model):
    COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('gray', 'Gray'),
        ('orange', 'Orange'),
        ('mixed', 'Mixed'),
    ]

    name = models.CharField(max_length=100, verbose_name='кличка')
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, verbose_name='цвет')
    age = models.PositiveIntegerField(verbose_name='возраст в месяцах')  # возраст в месяцах
    description = models.TextField(max_length=1000, verbose_name='описание', **NULLABLE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='kittens')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'котенок'
        verbose_name_plural = 'котята'
        ordering = ('pk',)


class Rating(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.kitten} - {self.rating}'

    class Meta:
        verbose_name = 'рейтинг'
        verbose_name_plural = 'рейтинги'
        ordering = ('pk',)
