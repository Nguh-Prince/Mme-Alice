from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register("candidates", views.CandidateViewSet, basename='candidates')
router.register("votes", views.VoteViewSet, basename='votes')
router.register("voteids", views.VoteIDViewSet, basename='voteid')
router.register("ids", views.IDCardViewSet, basename='ids')

urlpatterns = router.urls