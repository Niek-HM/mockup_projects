from django.views.generic import ListView
from django.db.models import Q

from ..models import Archive, Tag

class SearchArchiveView(ListView):
    """
    Here you can search through the Archive (pdf's) and view them at archiveView.
    The sorting is fine for now.
    """
    template_name = 'main/search_archive.html'
    context_object_name = 'items'
    model = Archive

    paginate_by = 20

    def get_queryset(self):
        # Get the search query from the URL parameter
        search_query = self.request.GET.get('search', '')
        tag = self.request.GET.get('tag', '')

        # Filter the queryset based on title or description containing the search query
        queryset = Archive.objects.filter(
            Q(name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(pdf__icontains=search_query),
            Q(tag__name__icontains=tag)
        )

        queryset = queryset.order_by('-name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get('search', '')
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag', '')

        return context