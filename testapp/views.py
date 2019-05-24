from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Person
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# Получение данных из БД
def index(request):
    try:
        getUser = Person.objects.all().order_by('-id')
    except:
        getUser = []
    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = 1
    if page == 1:
        paginator = Paginator(getUser, 10)
    else:
        paginator = Paginator(getUser, 5)
        page = int(page)+1
    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = []
    if not 'is_ajax' in request.GET:
        return render(request, "index.html", {"people": user_list})
    else:
        is_over = False
        if paginator.num_pages <= page:
            is_over = True
        user_json = []
        for item in user_list:
            user_json.append({
                'name': item.name,
                'phone': item.phone,
                'id': item.id,
            })
        return render(
            request,
            'ajax.html',
            {
                "ajax_json": json.dumps({
                    'list': user_json,
                    'is_over': is_over
                })
            }
        )

# Сохранение данных в БД
def create(request):
    if request.method == "POST":
        per = Person()
        per.name = request.POST.get("name")
        per.phone = request.POST.get("phone")
        per.save()
    return HttpResponseRedirect("/")

# Изменение данных в БД
def edit(request, id):
    try:
        person = Person.objects.get(id=id)
        if request.method == "POST":
            person.name = request.POST.get("name")
            person.phone = request.POST.get("phone")
            person.save()
            if not 'is_ajax' in request.POST:
                return HttpResponseRedirect("/")
            else:
                return render(
                    request,
                    'ajax.html',
                    {
                        "ajax_json": json.dumps({
                            'successRequest': True,
                            'userData': {
                                'name': person.name,
                                'phone': person.phone,
                            }
                        })
                    }
                )
        else:
            return render(request, "edit.html", {"person": person})
    except Person.DoesNotExist:
        if not 'is_ajax' in request.POST:
            return HttpResponseNotFound("<h2>Person not found</h2>")
        else:
            return render(
                request,
                'ajax.html',
                {
                    "ajax_json": json.dumps({
                        'successRequest': False,
                        'userData': {}
                    })
                }
            )


# Удаление данных из БД
def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
