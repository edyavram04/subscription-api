from django.urls import path
from .views import SubscriptionPlanList, ProtectedContent, UpgradeToPremium

urlpatterns = [
    path('plans/', SubscriptionPlanList.as_view(), name='plan-list'),
    path('secret/', ProtectedContent.as_view(), name='secret'), 
    
    # Ruta nouă pentru simularea plății
    path('upgrade/', UpgradeToPremium.as_view(), name='upgrade'),
]