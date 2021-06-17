from django.shortcuts import render, redirect
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from . import engine
import os
# path = str(os.getcwd()) + '\searchengine\templates\searchengine\Jan'


def index(request, pk=1):
    files = engine.create_file_list()
    # print("----", files)
    if request.method == 'GET':
        template = loader.get_template('searchengine/index.html')
        context = {'path':files}
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        return search(request)

def search(request):
    template = loader.get_template('searchengine/results.html')
    search_query = request.POST.get('search')
    query = search_query.lower()
    print('----query = ', query)
    bools = [' and ', ' or ', ' but ']
    # q = 'cat and html or dog or good'
    is_bool_query = False
    result_list = []
    for i in bools:
        if i in query:
            is_bool_query = True
    if is_bool_query:
        t = engine.bool_query(query)
        # t = engine.bool_query(query)
        print('_#__#__#_#__#__#_#_#')
        print(t)
        # url = t.rsplit('\\',1)
        # print(url)
        # result_list.append(url)
        # is_bool_query = True
        checker = []
        for result in t:
            # if len(t) > 1 and result not in checker:
            print('LOOP RUN ')
            if result not in checker:
                print('result =-----====---', result)
                url = result.rsplit('\\',1)
                print(url)
                result_list.append(url)
                checker.append(result)
            # else:
            #     print('result =-----====---', result)
            #     url = result.rsplit('\\',1)
            #     print(url)
            #     result_list.append(url)
            is_bool_query = True
        # break
    else:
        # is_bool_query = False
        pass
    if is_bool_query == False:
        if query != None and query.isnumeric() != True:
            t = engine.phrasal_query(query)
            t.sort(key=lambda x:x[1], reverse=True)
            
            for result in t:
                print(result[0])
                url = result[0].rsplit('\\',1)
                print(url)
                result_list.append(url)
        else:
            print('invalid search')
    if query == None or query == '':
        print('goooooodbye')
    print('result list --------------------------')
    values = []
    print('length of list ===== ', len(result_list))
    for i in result_list:
        print('-----dl;akjfsd;lkjafs;dlkj;laksdjf')
        print(i)
        print('-----dl;akjfsd;lkjafs;dlkj;laksdjf')
        print(i[1])
        values.append(i[1])
    url_name = []
    for v in values:
        name = v.rsplit('.',1)
        print(name[0])
        url_name.append(name[0])
    # print(result_list)
    results = result_list
    context = {
        'query': search_query,
        'results': values,
        'urls': url_name,
    }
    # search = request.POST.get('search')
    # results = 'pending'
    # context = {
    #     'search': search,
    #     'results': results,
    # }
    return HttpResponse(template.render(context, request))

def check(request):
    template=loader.get_template('searchengine/Jan/aol.html')

    # return redirect("https://youtu.be/dQw4w9WgXcQ?t=43")
    return HttpResponse(template.render({}, request))
