from django.views.generic import DetailView

from ..models import Archive

class ArchiveView(DetailView):
    """
    Display a specific PDF with it's title, pdf and give seo data to google.
    """
    template_name = 'main/specific_archive.html'

    context_object_name = 'item'
    model = Archive
    pk_url_kwarg = 'id'