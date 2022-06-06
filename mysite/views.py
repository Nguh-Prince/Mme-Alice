from django.db.models import Count
from django.db.models.functions import Coalesce
from django.utils.translation import gettext as _

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import copy
from mysite.models import Candidate, Vote, VoteID

from mysite.serializers import CandidateSerializer, VoteIDSerializer, VoteSerializer
from . import permissions
from rest_framework import permissions as perms

class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [perms.IsAuthenticatedOrReadOnly, permissions.ModelPermission]
    permission_classes = []
    queryset = Candidate.objects.all()

class VoteIDViewSet(viewsets.ModelViewSet):
    serializer_class = VoteIDSerializer
    permission_classes = [permissions.ModelPermission]
    permission_classes = []
    queryset = VoteID.objects.all()

class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsReadingOrPostingOrReadOnly]
    queryset = Vote.objects.all()

    @action(methods=['POST', ], detail=False)
    def vote(self, request):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        breakpoint()
        voteid = VoteID.objects.get(vote_code=validated_data.pop("vote_code"))
        instance = Vote.objects.create(voteid=voteid, candidate=validated_data.pop("candidate"))
        
        return Response(serializer(instance).data)

    @action(methods=['GET', ], detail=False)
    def statistics(self, request):
        statistics_base_dictionary = {
            "total_number_of_votes": 0
        }
        statistics_base_dictionary = {
            "general": {
                "total_number_of_votes": 0
            },
            "candidates": {}
        }

        dictionary_to_return = {
            "general": copy.deepcopy(statistics_base_dictionary),
            "daily": {}
        }
        queryset = Vote.objects.all()
        votes_aggregation = queryset.aggregate(total_votes=Coalesce(Count("id"), 0))

        dictionary_to_return["general"]["total_number_of_votes"] = votes_aggregation["total_votes"]

        votes_by_candidates_annotation = queryset.values("candidate").annotate(
            number_of_votes=Coalesce(Count("id"), 0)
        )

        votes_by_day_annotation = queryset.values("date_made").annotate(
            number_of_votes=Coalesce(Count("id"), 0)
        )

        votes_by_day_by_candidate_annotation = queryset.values("date_made", "candidate").annotate(
            number_of_votes=Coalesce(Count("id"), 0)
        )

        for item in ["general", "daily"]:
            if item == "general":
                dictionary_to_return["general"]["general"]["total_number_of_votes"] = votes_aggregation["total_votes"]
                
                for item in votes_by_candidates_annotation:
                    dictionary_to_return["general"]["candidates"][item['candidate']] = {}
                    dictionary_to_return["general"]["candidates"][item['candidate']] = {}
                    
                    dictionary_to_return["general"]["candidates"][item['candidate']]['total_number_of_votes'] = item['number_of_votes']
                
            if item == "daily":
                for day in votes_by_day_annotation:
                    date_string = day["date_made"].strftime("%Y-%m-%d")

                    dictionary_to_return["daily"][date_string] = copy.deepcopy(statistics_base_dictionary)

                    for subitem in ["general"]:
                        if subitem == "general":
                            dictionary_to_return["daily"][date_string]["general"]["total_number_of_votes"] = day['number_of_votes']

                for record in votes_by_day_by_candidate_annotation:
                    date_string = record["date_made"].strftime("%Y-%m-%d")

                    dictionary_item = dictionary_to_return["daily"][date_string] if date_string in dictionary_to_return["daily"] else copy.deepcopy(statistics_base_dictionary)

                    dictionary_item["candidates"][record['candidate']] = {}
                    
                    dictionary_item["candidates"][record['candidate']]["total_number_of_votes"] = record["number_of_votes"]

        return Response(data=dictionary_to_return)
