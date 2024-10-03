from rest_framework import viewsets
from .models import Breed, Kitten, Rating
from .serializers import BreedSerializer, KittenSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated


class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [IsAuthenticated]


class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        breed = self.request.query_params.get('breed')
        if breed:
            queryset = queryset.filter(breed__name=breed)
        return queryset

    def perform_update(self, serializer):
        if self.get_object().user == self.request.user:
            serializer.save()

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        kitten = Kitten.objects.get(pk=self.request.data.get('kitten'))
        serializer.save(user=self.request.user, kitten=kitten)
