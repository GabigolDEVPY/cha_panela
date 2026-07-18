from django.db import models

# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"Nome: {self.name}"

class ItemReservation(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="reservations")
    guest_name = models.CharField(max_length=100)
    guest_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} reservou {self.item.name}"