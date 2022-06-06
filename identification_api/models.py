from datetime import datetime
from decimal import MAX_EMAX
from platform import mac_ver
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

class Person(models.Model):
    surname: str = models.CharField(max_length=50)
    given_names: str = models.TextField()
    date_of_birth: datetime = models.DateField()
    place_of_birth: str = models.CharField(max_length=100)
    sex: str = models.CharField(choices=(
            ( "M", _("Male") ),
            ("F", _("Female"))
        ),
        max_length=5
    )
    height: float = models.FloatField()
    occupation: str = models.CharField(max_length=100)
    father = models.ForeignKey("self", related_name="fathered_children", on_delete=models.PROTECT, null=True)
    mother = models.ForeignKey("self", related_name="mothered_children", on_delete=models.PROTECT, null=True)

    def age(self) -> int:
        now = timezone.now()
        days = now.date() - self.date_of_birth

        return divmod(days.days, 365)[0]

    def __str__(self) -> str:
        return f"{super().__str__()} {self.surname} {self.given_names}"

class Identification(models.Model):
    person: Person = models.ForeignKey(Person, on_delete=models.PROTECT)
    date_of_issue: datetime = models.DateField(auto_now_add=True)
    date_of_expiration: datetime = models.DateField()
    identification_post: str = models.CharField(max_length=10)
    unique_identifier: str = models.CharField(max_length=100, unique=True)
    number: str = models.CharField(max_length=100)
    sm: str = models.CharField(max_length=6)
    signature = models.ImageField()
    address: str = models.CharField(max_length=100)
    image = models.ImageField()
    fingerprint = models.ImageField()