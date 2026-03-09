from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import SubscriptionPlan

class SubscriptionPlanTests(TestCase):
    def setUp(self):

        self.client = APIClient()
        

        SubscriptionPlan.objects.create(
            name="Test Premium", 
            price=15.99, 
            description="A fake plan used only for automated testing."
        )

    def test_get_plans_list(self):
        response = self.client.get('/api/plans/')
        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Premium")
        self.assertEqual(response.data[0]['price'], "15.99")