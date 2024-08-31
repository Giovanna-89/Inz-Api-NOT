from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from django.utils import timezone
from django.contrib.staticfiles.storage import staticfiles_storage
from io import BytesIO
from django.db import models
from core.models import Zadanie
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os

class RaportView(View):
    def get(self, request, *args, **kwargs):
        # Ustawienia odpowiedzi
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="raport.pdf"'

        # Utworzenie dokumentu PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Rejestracja fontu obsługującego polskie znaki
        font_path = os.path.join(settings.BASE_DIR, 'reports/static/reports/fonts/DejaVuSans.ttf')
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

        # Style
        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(name='Header', fontName='DejaVuSans', fontSize=18, leading=22, spaceAfter=20, alignment=1, textColor=colors.HexColor("#1F4D8E"))
        subheader_style = ParagraphStyle(name='SubHeader', fontName='DejaVuSans', fontSize=16, leading=20, spaceAfter=10, textColor=colors.HexColor("#333333"))
        normal_style = ParagraphStyle(name='CustomNormal', fontName='DejaVuSans', fontSize=12, leading=14, textColor=colors.HexColor("#666666"))

        # # Dodanie logo
        # try:
        #     logo_path = staticfiles_storage.path('images/logo.png')
        #     logo = Image(logo_path, width=1.5 * inch, height=0.75 * inch)
        #     story.append(logo)
        # except:
        #     pass  # Jeśli logo nie zostanie znalezione, kontynuuj bez niego

        # Nagłówek
        story.append(Paragraph("Raport Przetargów", header_style))

        # Informacje o przetargach
        liczba_przetargow = Zadanie.objects.count()
        story.append(Paragraph(f"Liczba przetargów: {liczba_przetargow}", subheader_style))

        # Tabela z danymi 
        data = [['Rodzaj zadania', 'Status', 'Liczba']]
        zadania = Zadanie.objects.values('rodzaj_zadania__nazwa', 'status__nazwa').annotate(count=models.Count('id'))

        for zadanie in zadania:
            data.append([zadanie['rodzaj_zadania__nazwa'], zadanie['status__nazwa'], str(zadanie['count'])])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F4F0EC")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#333333")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#E0F2F1")),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#666666")),
        ]))
        story.append(table)

        # Dodanie przerwy przed stopką
        story.append(Spacer(1, 2 * inch))

        # Dodanie stopki z informacją o generowaniu raportu
        current_time = timezone.now().strftime("%d-%m-%Y %H:%M:%S")
        user_info = f"Wygenerowane przez: {request.user.first_name} {request.user.last_name}, {current_time}"
        story.append(Paragraph(user_info, normal_style))

        # Budowanie dokumentu
        doc.build(story)

        response.write(buffer.getvalue())
        buffer.close()
        return response
