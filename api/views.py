from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection

from .models import SubscriptionPlan, UserProfile
from .serializers import SubscriptionPlanSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class SubscriptionPlanList(APIView):
    # The GET function is triggered when someone accesses the URL to read data
    def get(self, request):
        # 1. Fetch all plans from the database
        plans = SubscriptionPlan.objects.all()
        
        # 2. Pass them through the Translator (Serializer)
        serializer = SubscriptionPlanSerializer(plans, many=True)
        
        # 3. Return them as a valid JSON response for the web
        return Response(serializer.data)
    
class ProtectedContent(APIView):
    # This acts as a guard. It blocks access if you don't have a token!
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            # 1. Find the profile of the user making the request
            profile = UserProfile.objects.get(user=request.user)
            
            # 2. Check which plan they have
            if profile.plan and profile.plan.name == 'Premium':
                return Response({
                    "message": f"Hello, {request.user.username}! You have VIP access to the exclusive Gaming and AI content."
                })
            else:
                # HTTP 403 means "I know who you are, but you are not allowed here"
                return Response({
                    "error": "Access denied. You need a Premium subscription."
                }, status=403) 
                
        except UserProfile.DoesNotExist:
            return Response({
                "error": "Your account does not have an active subscriber profile."
            }, status=404)
        
class UpgradeToPremium(APIView):
    # Only logged-in users can attempt to pay
    permission_classes = [IsAuthenticated]

    # We use POST because we are modifying data on the server (performing an upgrade)
    def post(self, request):
        try:
            # 1. Find the user's profile and the Premium plan in the database
            profile = UserProfile.objects.get(user=request.user)
            premium_plan = SubscriptionPlan.objects.get(name='Premium')
            
            # 2. Check if they are already a Premium user
            if profile.plan == premium_plan:
                return Response({"message": "You are already a Premium user!"})
            
            # 3. In real life, this is where the code to communicate with Stripe/Bank would go.
            # Here, we simulate an instantly approved payment and change their plan:
            profile.plan = premium_plan
            profile.save() # Save the change in PostgreSQL
            
            return Response({
                "message": f"Congratulations, {request.user.username}! The payment was processed. You have been upgraded to Premium 🚀."
            })
            
        except UserProfile.DoesNotExist:
            return Response({"error": "Your profile was not found."}, status=404)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "The Premium plan is not configured in the system."}, status=404)

class SubscriptionStats(APIView):
    # Only authenticated users (like admins) should see this
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # We write raw SQL to join tables and count users per plan
        # Django automatically names tables as: appname_modelname
        sql_query = """
            SELECT sp.name, COUNT(up.id) as user_count
            FROM api_subscriptionplan sp
            LEFT JOIN api_userprofile up ON sp.id = up.plan_id
            GROUP BY sp.name;
        """
        
        # Open a direct cursor to PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall() # Get all results
            
        # Format the raw database rows into a nice JSON list
        # row[0] is the plan name (sp.name), row[1] is the count
        stats = [
            {"plan_name": row[0], "total_users": row[1]} 
            for row in rows
        ]
        
        return Response({"statistics": stats})
    
class RegisterUser(APIView):
    # Anyone should be able to register, so we don't require a token here
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        # Check if the username already exists in the database
        if User.objects.filter(username=username).exists():
            return Response({"error": "This username is already taken."}, status=400)

        # 1. Create the new user and encrypt their password
        new_user = User.objects.create(
            username=username,
            password=make_password(password) # Always encrypt passwords!
        )

        # 2. Assign them the default 'Free' plan
        try:
            free_plan = SubscriptionPlan.objects.get(name='Free')
        except SubscriptionPlan.DoesNotExist:
            free_plan = None # Fallback just in case the 'Free' plan doesn't exist

        # 3. Create their profile
        UserProfile.objects.create(user=new_user, plan=free_plan)

        return Response({
            "message": f"Success! Account for {username} was created. You can now log in."
        }, status=201)