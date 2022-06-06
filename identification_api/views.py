# from requests import requet
from rest_framework import viewsets
from . import serializers, models

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    permission_classes = []
    queryset = models.Person.objects.all()

class IdentifictionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IdentificationSerializer
    permission_classes = []
    
    def get_queryset(self):
        query = models.Identification.objects.all()

        if "parent_lookup_person" in self.kwargs:
            query = query.filter( id=self.kwargs["parent_lookup_person"] )

        return query

    def list(self, request):
        queryset = self.get_queryset()
        
        if "name" in request.GET:
            name = request.GET["name"]

            queryset = queryset.filter(name__icontains=name)

        if "surname" in request.GET:
            surname = request.GET["surname"]

            queryset = queryset.filter(surname__icontains=surname)