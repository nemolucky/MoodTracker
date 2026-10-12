from django.http import HttpResponse


def moods(request):
    return HttpResponse("Список настроений")


def mood_detail(request, mood_id):
    return HttpResponse(f"Настроение {mood_id}")
