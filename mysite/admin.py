from django.contrib import admin
from .models import Item, ItemReservation
# Register your models here.

@admin.register(Item)
class ItemPainel(admin.ModelAdmin):
    list_display = ("name", "active")
    fieldsets = (
        (None, {"fields": ("name", "active", "quantity")}),
        ("Fotos do produto", {"fields": ("foto", "foto2", "foto3")}),
    )

@admin.register(ItemReservation)
class ItemReservationPainel(admin.ModelAdmin):
    list_display = ("item", "guest_name", "guest_phone", "created_at")
    list_filter = ("item", "created_at")
    search_fields = ("guest_name", "guest_phone")