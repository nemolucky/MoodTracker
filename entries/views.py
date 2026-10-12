from django.http import HttpResponse


def entries(request):
    return HttpResponse("Список записей")


def entry_detail(request, entry_id):
    return HttpResponse(f"Запись {entry_id}")
