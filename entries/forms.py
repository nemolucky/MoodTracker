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


class EntryForm(forms.ModelForm):
    """Редактор дневника с явным списком разрешённых полей."""
    class Meta:
        from .models import MoodEntry
        model = MoodEntry
        fields = ("user", "entry_date", "score", "mood", "factors", "comment")
        widgets = {
            "entry_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}),
            "comment": forms.Textarea(attrs={"rows": 4}),
            "score": forms.NumberInput(attrs={"min": 0, "max": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_entry_date(self):
        from django.utils import timezone
        date = self.cleaned_data["entry_date"]
        if date > timezone.localdate():
            raise forms.ValidationError("Дата записи не может быть в будущем.")
        return date

    def clean_comment(self):
        return self.cleaned_data["comment"].strip()

    def clean(self):
        data = super().clean()
        if data.get("score") is not None and data["score"] <= 3:
            if not data.get("comment"):
                raise forms.ValidationError(
                    "При оценке 0–3 добавьте комментарий о своём состоянии.")
        return data
