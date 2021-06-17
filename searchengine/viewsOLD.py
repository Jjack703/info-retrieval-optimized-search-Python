from django.shortcuts import render, redirect
from django.template import loader

# Create your views here.
from django.http import HttpResponse

def index(request, pk=1):
    if request.method == 'GET':
        template = loader.get_template('searchengine/index.html')
        context = {}
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        return search(request)

def search(request):
    template = loader.get_template('searchengine/results.html')
    search = request.POST.get('search')
    results = 'pending'
    context = {
        'search': search,
        'results': results,
    }
    return HttpResponse(template.render(context, request))

def check(request):
    print('checking request info')
    print(request.data)
    template=loader.get_template('searchengine/Jan/galant.html')

    return redirect("https://youtu.be/dQw4w9WgXcQ?t=43")
    # return HttpResponse(template.render({}, request))
