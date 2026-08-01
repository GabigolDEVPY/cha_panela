from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    quantity = models.IntegerField()
    foto = models.ImageField(upload_to="items/", null=True, blank=True, verbose_name="Foto 1")
    foto2 = models.ImageField(upload_to="items/", null=True, blank=True, verbose_name="Foto 2")
    foto3 = models.ImageField(upload_to="items/", null=True, blank=True, verbose_name="Foto 3")

    def get_fotos(self):
        fotos = []
        for field in ("foto", "foto2", "foto3"):
            img = getattr(self, field, None)
            if img:
                fotos.append(img.url)
        return fotos

    def __str__(self):
        return f"Nome: {self.name}"

class ItemReservation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reservations")
    guest_name = models.CharField(max_length=100)
    guest_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} reservou {self.item.name}"