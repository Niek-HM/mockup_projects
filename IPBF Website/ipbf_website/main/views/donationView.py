from django.views.generic import TemplateView

class DonationView(TemplateView):
    """
    Simple donation page, make sure paypall works correctly!
    """
    template_name = 'main/donation.html'