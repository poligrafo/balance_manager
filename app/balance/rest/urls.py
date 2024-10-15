from rest_framework.routers import DefaultRouter

from app.balance.rest.views import BalanceViewSet

router = DefaultRouter()
router.register(r'balance', BalanceViewSet, basename='balance')

urlpatterns = router.urls
