from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from django.utils import timezone
from io import BytesIO
from core.models import Zadanie
import os

class ZadaniePDFBuilder:
    def __init__(self, user):
        self.user = user

    def build_pdf(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Czcionki
        font_path = os.path.join(settings.BASE_DIR, 'reports/static/reports/fonts/DejaVuSans.ttf')
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

        # Style
        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(name='Header', fontName='DejaVuSans', fontSize=18, leading=22, spaceAfter=20, alignment=1, textColor=colors.HexColor("#1F4D8E"))
        subheader_style = ParagraphStyle(name='SubHeader', fontName='DejaVuSans', fontSize=16, leading=20, spaceAfter=10, textColor=colors.HexColor("#333333"))
        normal_style = ParagraphStyle(name='CustomNormal', fontName='DejaVuSans', fontSize=12, leading=14, textColor=colors.HexColor("#666666"))

        # Nagłówek
        story.append(Paragraph("Raport Przetargów", header_style))

        # Liczba przetargów
        liczba_przetargow = Zadanie.objects.count()
        story.append(Paragraph(f"Liczba przetargów: {liczba_przetargow}", subheader_style))

        # Tabela
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

        # Stopka
        story.append(Spacer(1, 2 * inch))
        current_time = timezone.now().strftime("%d-%m-%Y %H:%M:%S")
        user_info = f"Wygenerowane przez: {self.user.first_name} {self.user.last_name}, {current_time}"
        story.append(Paragraph(user_info, normal_style))

        doc.build(story)
        buffer.seek(0)
        return buffer
