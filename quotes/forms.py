from django import forms
from django.db import models
from django.utils.text import slugify
from .models import Quote, Source
from .utils import normalize_text

class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(
        max_length=255,
        label="Источник",
        help_text="Введите название источника (например, название книги или фильма)."
    )

    class Meta:
        model = Quote
        fields = ['source_name', 'quote', 'weight']

    def clean(self):
        cleaned_data = super().clean()
        source_name = cleaned_data.get('source_name')
        quote = cleaned_data.get('quote')

        if source_name and quote:
            # Создание или нахождение источника
            source, created = Source.objects.get_or_create(
                name=source_name,
                defaults={'slug': slugify(source_name)}  # Генерация слага
            )
            cleaned_data['source'] = source

            # Нормализование текста цитаты
            normalized_quote = normalize_text(quote)

            # Проверка на дубликаты цитат
            if Quote.objects.filter(source=source, normalized_quote=normalized_quote).exists():
                raise forms.ValidationError("Цитата уже существует.")

            # Проверка количества цитат от одного источника
            if Quote.objects.filter(source=source).count() >= 3:
                raise forms.ValidationError("У этого источника уже есть 3 цитаты.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.source = self.cleaned_data['source']
        if commit:
            instance.save()
        return