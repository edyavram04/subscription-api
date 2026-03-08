from django.urls import path
from .views import SubscriptionPlanList, ProtectedContent, UpgradeToPremium, SubscriptionStats, RegisterUser

urlpatterns = [
    path('plans/', SubscriptionPlanList.as_view(), name='plan-list'),
    path('secret/', ProtectedContent.as_view(), name='secret'), 
    path('upgrade/', UpgradeToPremium.as_view(), name='upgrade'),
    path('stats/', SubscriptionStats.as_view(), name='stats'),
    
    # New route for user registration
    path('register/', RegisterUser.as_view(), name='register'),
]