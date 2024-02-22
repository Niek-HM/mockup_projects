from django.urls import path
from django.views.generic import RedirectView

from .views import (HomeView, 
                    DonationView,
                    DisclaimerCopyrightView,
                    ContactView,
                    ArchiveView, 
                    SearchArchiveView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('donations/', DonationView.as_view(), name='donations'),
    path('disclaimer_copyright/', DisclaimerCopyrightView.as_view(), name="disclaimer_copyright"),
    path('contact/', ContactView.as_view(), name='contact'),

    path('archive/search/', SearchArchiveView.as_view(), name="search_archive"),
    path('archive/<int:id>/', ArchiveView.as_view()),

    path('pdf-2/IPBF_Brochure_IC-BPS_Diagnosis&Treatment.pdf', RedirectView.as_view(url='/archive/3170/'), name='redirect_to_brochure'),
]