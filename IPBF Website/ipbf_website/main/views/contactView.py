from django.views.generic import TemplateView

class ContactView(TemplateView):
    """
    Simple contact information page
    """
    template_name = 'main/contact.html'