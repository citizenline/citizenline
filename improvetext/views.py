
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse

from .models import Improvetext

def index(request):
    latest_text_list = Improvetext.objects.order_by('-pub_date')[:5]
    context = RequestContext(request, {
        'latest_text_list': latest_text_list,
    })
    return render(request, 'improvetext/index.html', context)

def detail(request, improvetext_id):
    improvetext = get_object_or_404(Improvetext, pk=improvetext_id)
    return render(request, 'improvetext/detail.html', {'improvetext': improvetext})

def results(request, improvetext_id):
    response = "You're looking at the results of text %s."
    return HttpResponse(response % improvetext_id)

def vote(request, improvetext_id):
    return HttpResponse("You're voting on text %s." % improvetext_id)