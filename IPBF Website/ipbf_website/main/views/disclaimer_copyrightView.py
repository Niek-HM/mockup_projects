from django.views.generic import TemplateView

class DisclaimerCopyrightView(TemplateView):
    """
    Simple disclaimer/Copyright page
    """
    template_name = 'main/disclaimer_copyright.html'