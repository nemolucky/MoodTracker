"""Проверка параметров списка и поиска."""
from django import forms
from moods.models import Mood


class EntryFilterForm(forms.Form):
    q = forms.CharField(required=False, max_length=200, label="Поиск")
    date = forms.DateField(required=False, label="Дата",
                           widget=forms.DateInput(attrs={"type": "date"}))
    mood = forms.ModelChoiceField(
        queryset=Mood.objects.all(), required=False, label="Настроение")
    min_score = forms.IntegerField(
        required=False, min_value=0, max_value=10, label="Оценка от")
    sort = forms.ChoiceField(required=False, label="Сортировка", choices=[
        ("", "Сначала новые"), ("date", "Сначала старые"),
        ("score", "По оценке"), ("user", "По пользователю")])
