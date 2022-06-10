from django.db import models

import random
import string

from django.contrib.auth.models import AbstractUser

def generate_vote_code():
    code = random.choices( string.ascii_lowercase + string.digits, k=10 )

    while VoteID.objects.filter(vote_code=code).exists():
        code = random.choices( string.ascii_lowercase + string.digits, k=10 )
    
    return ''.join(code)

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    party = models.CharField(max_length=255)
    statement = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"

    def get_candidates(self):
        return self.__class__.objects.annotate(number_of_votes=Count( Vote.objects.filter(candidate__id=OuterRef("id") ).values("id") )).order_by("-number_of_votes")

    @property
    def position(self):
        candidates = list(self.get_candidates())

        try:
            return candidates.index(self) + 1
        except ValueError as e:
            raise e

    @property
    def number_of_votes(self) -> int:
        return self.vote_set.count()

    @property
    def vote_percentage(self) -> float:
        number_of_votes = self.number_of_votes
        total_number_of_votes = Vote.objects.all().count()

        return (number_of_votes / total_number_of_votes) * 100

class IDCard(models.Model):
    number = models.CharField(max_length=30, unique=True)

class VoteID(models.Model):
    vote_code = models.CharField(max_length=255, unique=True, default=generate_vote_code)
    idcard = models.OneToOneField(IDCard, on_delete=models.CASCADE, null=True)
    idcard_num = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if self.idcard:
            self.idcard_num = self.idcard.number
            
        return super().save(*args, **kwargs)

class Vote(models.Model):
    voteid = models.OneToOneField(VoteID, on_delete=models.PROTECT, unique=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT)
    time_made = models.DateTimeField(auto_now_add=True)
    date_made = models.DateField(auto_now_add=True)