from django.views.generic import TemplateView

class HomeView(TemplateView):
    """
    This is the Home page, it is the only place i use the Editable texts.
    Might use it on places like contacts/donations/copyright_disclaimer
    """
    template_name = 'main/home.html'