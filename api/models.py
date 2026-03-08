from django.db import models

from django.db import models
from django.contrib.auth.models import User

# Tabelul pentru planurile de abonament (ex: Free, Premium)
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50) 
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

# Tabelul care extinde utilizatorul standard cu detalii despre abonamentul lui
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username