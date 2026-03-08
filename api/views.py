from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer
from rest_framework.permissions import IsAuthenticated
from .models import SubscriptionPlan, UserProfile

class SubscriptionPlanList(APIView):
    # Funcția GET se activează când cineva accesează URL-ul pentru a citi date
    def get(self, request):
        # 1. Luăm toate planurile din baza de date
        plans = SubscriptionPlan.objects.all()
        # 2. Le trecem prin Traducător (Serializer)
        serializer = SubscriptionPlanSerializer(plans, many=True)
        # 3. Le returnăm sub formă de răspuns valid pentru internet
        return Response(serializer.data)
    
class ProtectedContent(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            # 1. Căutăm profilul utilizatorului care a făcut cererea
            profile = UserProfile.objects.get(user=request.user)
            
            # 2. Verificăm ce plan are
            if profile.plan and profile.plan.name == 'Premium':
                return Response({
                    "message": f"Salut, {request.user.username}! Ai acces VIP la conținutul exclusiv de Gaming și AI."
                })
            else:
                # HTTP 403 înseamnă "Te cunosc, dar nu ai voie aici"
                return Response({
                    "error": "Acces interzis. Ai nevoie de un abonament Premium."
                }, status=403) 
                
        except UserProfile.DoesNotExist:
            return Response({
                "error": "Contul tău nu are un profil de abonat setat."
            }, status=404)
        
class UpgradeToPremium(APIView):
    # Doar userii logați pot încerca să plătească
    permission_classes = [IsAuthenticated]

    # Folosim POST pentru că modificăm date pe server (facem un upgrade)
    def post(self, request):
        try:
            # 1. Găsim profilul utilizatorului și planul Premium în baza de date
            profile = UserProfile.objects.get(user=request.user)
            premium_plan = SubscriptionPlan.objects.get(name='Premium')
            
            # 2. Verificăm dacă nu cumva e deja Premium
            if profile.plan == premium_plan:
                return Response({"message": "Ești deja utilizator Premium!"})
            
            # 3. Aici, în viața reală, ar fi codul care comunică cu Stripe sau banca.
            # Noi simulăm o plată aprobată instantaneu și îi schimbăm planul:
            profile.plan = premium_plan
            profile.save() # Salvăm modificarea în PostgreSQL
            
            return Response({"message": f"Felicitări, {request.user.username}! Plata a fost procesată. Ai fost upgradat la Premium 🚀."})
            
        except UserProfile.DoesNotExist:
            return Response({"error": "Profilul tău nu a fost găsit."}, status=404)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Planul Premium nu este configurat în sistem."}, status=404)