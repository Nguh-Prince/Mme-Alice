from rest_framework import serializers
from django.utils.translation import gettext as _

from mysite.models import Candidate, IDCard, Vote, VoteID

class CandidateSerializer(serializers.ModelSerializer):
    image = serializers.CharField(allow_null=True, allow_blank=True)
    class Meta:
        model = Candidate
        fields = ("id", "name", "party", "statement", "image", "age")
        extra_kwargs = {"image": {"required": False, "allow_blank": True}}

class VoteIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteID
        fields = ("vote_code", "idcard_num")
        extra_kwargs = {"vote_code": {"allow_null": True, "allow_blank": True, "required": False, "read_only": True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

class VoteSerializer(serializers.ModelSerializer):
    vote_code = serializers.CharField(write_only=True)
    
    class Meta:
        model = Vote
        fields = ("voteid", "candidate", "vote_code")
        extra_kwargs = {"voteid": {"allow_null": True, "required": False}}

    def validate_voteid(self, data):
        if self.Meta.model.objects.filter(voteid=data).exists():
            raise serializers.ValidationError(
                _("This voter has already voted")
            )
        return data

    def validate_vote_code(self, data):
        if not VoteID.objects.filter(vote_code=data).exists():
            raise serializers.ValidationError( _("No voter exists with code %(code)s" % {'code': data}) )
        if self.Meta.model.objects.filter(voteid__vote_code=data).exists():
            raise serializers.ValidationError(
                _("This voter has already voted")
            )
        return data

    def create(self, validated_data):
        breakpoint()
        voteid = VoteID.objects.get(vote_code=validated_data.pop("vote_code"))
        instance = Vote.objects.create(voteid=voteid, candidate=validated_data.pop("candidate"))
        breakpoint()

        return instance

class IDCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDCard
        fields = ("id", "number")