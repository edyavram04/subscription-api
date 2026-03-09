from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection

from .models import SubscriptionPlan, UserProfile
from .serializers import SubscriptionPlanSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class SubscriptionPlanList(APIView):
    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        
        serializer = SubscriptionPlanSerializer(plans, many=True)

        return Response(serializer.data)
    
class ProtectedContent(APIView):

    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:

            profile = UserProfile.objects.get(user=request.user)
            

            if profile.plan and profile.plan.name == 'Premium':
                return Response({
                    "message": f"Hello, {request.user.username}! You have VIP access to the exclusive Gaming and AI content."
                })
            else:
  
                return Response({
                    "error": "Access denied. You need a Premium subscription."
                }, status=403) 
                
        except UserProfile.DoesNotExist:
            return Response({
                "error": "Your account does not have an active subscriber profile."
            }, status=404)
        
class UpgradeToPremium(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):
        try:

            profile = UserProfile.objects.get(user=request.user)
            premium_plan = SubscriptionPlan.objects.get(name='Premium')
            

            if profile.plan == premium_plan:
                return Response({"message": "You are already a Premium user!"})
            

            profile.plan = premium_plan
            profile.save() 
            
            return Response({
                "message": f"Congratulations, {request.user.username}! The payment was processed. You have been upgraded to Premium 🚀."
            })
            
        except UserProfile.DoesNotExist:
            return Response({"error": "Your profile was not found."}, status=404)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "The Premium plan is not configured in the system."}, status=404)

class SubscriptionStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sql_query = """
            SELECT sp.name, COUNT(up.id) as user_count
            FROM api_subscriptionplan sp
            LEFT JOIN api_userprofile up ON sp.id = up.plan_id
            GROUP BY sp.name;
        """
        

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall() 
            

        stats = [
            {"plan_name": row[0], "total_users": row[1]} 
            for row in rows
        ]
        
        return Response({"statistics": stats})
    
class RegisterUser(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "This username is already taken."}, status=400)


        new_user = User.objects.create(
            username=username,
            password=make_password(password)
        )

        try:
            free_plan = SubscriptionPlan.objects.get(name='Free')
        except SubscriptionPlan.DoesNotExist:
            free_plan = None 


        UserProfile.objects.create(user=new_user, plan=free_plan)

        return Response({
            "message": f"Success! Account for {username} was created. You can now log in."
        }, status=201)