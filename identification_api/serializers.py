from rest_framework import serializers

from identification_api.models import Identification, Person

simple_person_fields = (
        "id", "surname", "given_names", "date_of_birth", "place_of_birth", "sex", "height", "occupation", "age"
    )

simple_identification_fields = ("date_of_issue", "date_of_expiration", "identification_post", "unique_identifier", "number", "sm", "signature", "address", "image", "fingerprint" )

class PersonSerializer(serializers.ModelSerializer):
    class ParentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Person
            fields = simple_person_fields
            extra_kwargs = {"age": {"read_only": True}}

    mother = ParentSerializer(allow_null=True, required=False)
    father = ParentSerializer(allow_null=True, required=False)

    class Meta:
        model = Person
        fields = simple_person_fields + ( "mother", "father" )
    
    def create(self, validated_data):
        mother = validated_data.pop("mother")
        father = validated_data.pop("father")

        mother_query = Person.objects.filter(**mother)
        father_query = Person.objects.filter(**father)

        if mother_query.exists():
            mother = mother_query.first()
        else:
            mother = Person.objects.create(**mother)

        if father_query.exists():
            father = father_query.first()
        else:
            father = Person.objects.create(**father)

        person = Person.objects.create(**validated_data, mother=mother, father=father)

        return person

class IdentificationSerializer(serializers.ModelSerializer):
    person_detail = PersonSerializer(source="person", read_only=True)

    class Meta:
        model = Identification
        fields = simple_identification_fields + ("person", "person_detail")