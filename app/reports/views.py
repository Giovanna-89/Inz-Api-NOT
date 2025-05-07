from django.http import HttpResponse
from django.views import View
from reports.builders.zadanie_pdf_builder import ZadaniePDFBuilder

class RaportView(View):
    def get(self, request, *args, **kwargs):
        builder = ZadaniePDFBuilder(request.user)
        pdf_buffer = builder.build_pdf()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="raport.pdf"'
        response.write(pdf_buffer.getvalue())
        return response