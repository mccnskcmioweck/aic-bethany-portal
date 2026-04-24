from django.shortcuts import render, get_object_or_404
from .models import Sermon
def sermon_list(request):
    return render(request, 'sermons/sermon_list.html', {'sermons': Sermon.objects.all()})
def sermon_detail(request, pk):
    return render(request, 'sermons/sermon_detail.html', {'sermon': get_object_or_404(Sermon, pk=pk)})
