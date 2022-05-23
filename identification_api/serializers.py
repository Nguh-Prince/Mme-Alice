from rest_framework import serializers

from identification_api.models import Person

simple_person_fields = (
        "id", "surname", "given_names", "date_of_birth", "place_of_birth", "sex", "height", "occupation", "age"
    )

class PersonSerializer(serializers.ModelSerializer):
    class ParentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Person
            fields = simple_person_fields
            extra_kwargs = {"age": {"read_only": True}}

    mother = ParentSerializer
    father = ParentSerializer

    class Meta:
        model = Person
        fields = simple_person_fields + ( "mother", "father" )