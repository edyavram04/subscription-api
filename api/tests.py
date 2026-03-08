from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import SubscriptionPlan

class SubscriptionPlanTests(TestCase):
    def setUp(self):
        # This setup function runs automatically BEFORE every test.
        # We use it to create a fake, isolated database just for testing.
        self.client = APIClient()
        
        # Let's create a temporary plan in our test database
        SubscriptionPlan.objects.create(
            name="Test Premium", 
            price=15.99, 
            description="A fake plan used only for automated testing."
        )

    def test_get_plans_list(self):
        # 1. Simulate a user making a GET request to our plans endpoint
        response = self.client.get('/api/plans/')
        
        # 2. Check if the server responded with a success status (200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 3. Check if the fake plan we created actually appears in the JSON response
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Premium")
        self.assertEqual(response.data[0]['price'], "15.99")