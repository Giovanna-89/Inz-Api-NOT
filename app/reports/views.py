from django.http import HttpResponse
from django.views import View
from reportlab.pdfgen import canvas
from core.models import Zadanie

class RaportView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="raport.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, "Raport Przetargów")

        p.drawString(100, 780, f"Liczba przetargów: {Zadanie.objects.count()}")
        

        p.showPage()
        p.save()
        return response
