from django.http import HttpResponse


def index(request):
    return HttpResponse("Mood Tracker — дневник настроения")
