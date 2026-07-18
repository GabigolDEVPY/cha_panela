from django.shortcuts import render, get_object_or_404
from .models import Items, ItemReservation
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models import Count

# Create your views here.

class Home(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Items.objects.filter(active=True).annotate(reservations_count=Count('reservations'))
        
        for item in items:
            item.available_quantity = item.quantity - item.reservations_count
            item.is_available = item.available_quantity > 0

        context["items"] = items
        return context

def confirmar_presente(request):
    if request.method == "POST":
        if request.session.get('presente_confirmado'):
            return HttpResponse('<div class="confirmacao-mensagem" style="display: block; background: #d4edda; color: #155724; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #c3e6cb; margin-top: 20px;"><p>Você já confirmou um presente! Muito obrigado.</p></div>')
        
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        item_id = request.POST.get('presente')
        
        if item_id:
            item = get_object_or_404(Items, id=item_id)
            current_reservations = item.reservations.count()
            
            if current_reservations >= item.quantity or not item.active:
                return HttpResponse('<div class="confirmacao-mensagem" style="display: block; background: #f8d7da; color: #721c24; padding: 20px; border-radius: 8px; border: 1px solid #f5c6cb;"><p>Desculpe, este presente já foi escolhido por todas as pessoas possíveis ou não está mais disponível.</p></div>')

            ItemReservation.objects.create(
                item=item,
                guest_name=nome,
                guest_phone=telefone
            )
            
            request.session['presente_confirmado'] = True
            request.session.set_expiry(500 * 24 * 60 * 60)
            
            return HttpResponse(f'''
            <div class="confirmacao-mensagem" style="display: block; background: #d4edda; color: #155724; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #c3e6cb; margin-top: 20px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px; color: #28a745;">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <h3 style="margin-bottom: 10px; color: #155724;">Presente Confirmado!</h3>
                <p>Muito obrigado, <strong>{nome}</strong>! Você escolheu: <strong>{item.name}</strong>.</p>
                <p>Recebemos sua confirmação. Mal podemos esperar para celebrar com você!</p>
            </div>
            ''')
    return HttpResponse("Método não permitido", status=405)