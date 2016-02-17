from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse

from .models import Text


def index(request):
    latest_text_list = Text.objects.order_by('-pub_date')[:5]
    context = RequestContext(request, {
        'latest_text_list': latest_text_list,
    })
    return render(request, 'bettertexts/index.html', context)


def detail(request, slug):
    text = get_object_or_404(Text, slug=slug)
    return render(request, 'bettertexts/detail.html', {'text': text})


def results(request, text_id):
    response = "You're looking at the results of text %s."
    return HttpResponse(response % text_id)


def vote(request, text_id):
    return HttpResponse("You're voting on text %s." % text_id)
