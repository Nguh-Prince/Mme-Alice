from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register("candidates", views.CandidateViewSet, basename='candidates')
router.register("votes", views.VoteViewSet, basename='votes')
router.register("voteid", views.VoteIDViewSet, basename='voteid')

urlpatterns = router.urls