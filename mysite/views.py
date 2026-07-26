from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count

from .models import Item, ItemReservation


class Home(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.filter(active=True).annotate(reservations_count=Count("reservations"))

        for item in items:
            item.available_quantity = item.quantity - item.reservations_count
            item.is_available = item.available_quantity > 0

        context["items"] = items
        return context


def confirmar_presente(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Metodo nao permitido."},
            status=405,
        )

    if request.session.get("presente_confirmado"):
        return JsonResponse({
            "success": True,
            "already_confirmed": True,
            "message": "Voce ja confirmou um presente. Muito obrigado!",
            "guest_name": request.session.get("convidado_nome", ""),
            "gift_name": request.session.get("presente_nome", ""),
            "gift_image": request.session.get("presente_foto", ""),
        })

    nome = request.POST.get("nome")
    telefone = request.POST.get("telefone")
    item_id = request.POST.get("presente")

    if not nome or not telefone or not item_id:
        return JsonResponse(
            {
                "success": False,
                "message": "Preencha seu nome, telefone e escolha um presente.",
            },
            status=400,
        )

    item = Item.objects.filter(id=item_id).first()
    if item is None:
        return JsonResponse(
            {
                "success": False,
                "message": "Presente nao encontrado.",
            },
            status=404,
        )

    current_reservations = item.reservations.count()

    if current_reservations >= item.quantity or not item.active:
        return JsonResponse(
            {
                "success": False,
                "message": "Desculpe, este presente ja foi escolhido por todas as pessoas possiveis ou nao esta mais disponivel.",
            },
            status=409,
        )

    ItemReservation.objects.create(
        item=item,
        guest_name=nome,
        guest_phone=telefone,
    )

    gift_image = item.foto.url if item.foto else ""
    request.session["presente_confirmado"] = True
    request.session["presente_nome"] = item.name
    request.session["presente_foto"] = gift_image
    request.session["convidado_nome"] = nome
    request.session.set_expiry(200 * 24 * 60 * 60)

    return JsonResponse({
        "success": True,
        "already_confirmed": False,
        "message": "Presente confirmado!",
        "guest_name": nome,
        "gift_name": item.name,
        "gift_image": gift_image,
    })
