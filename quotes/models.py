import random
from django.db import models
from .utils import unique_slugify, normalize_text

class Source(models.Model):
    name = models.CharField(max_length=255, verbose_name="Источник")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"

    def save(self, *args, **kwargs):
        """Сохранение полей модели при их отсутствии заполнения."""
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes', verbose_name="Источник")
    quote = models.TextField(verbose_name="Цитата")
    normalized_quote = models.CharField(max_length=255, verbose_name="Нормализованная цитата", editable=False)
    weight = models.PositiveIntegerField(default=1, verbose_name="Вес")
    likes = models.IntegerField(default=0, verbose_name="Лайки")
    dislikes = models.IntegerField(default=0, verbose_name="Дизлайки")
    views = models.IntegerField(default=0, verbose_name="Просмотры")

    def save(self, *args, **kwargs):
        # Нормализация текста перед сохранением
        self.normalized_quote = normalize_text(self.quote)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.source.name}: {self.quote[:50]}..."

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
        constraints = [
            models.UniqueConstraint(fields=['source', 'normalized_quote'], name='unique_normalized_quote_per_source'),
            models.CheckConstraint(check=models.Q(weight__gte=1), name='weight_gte_1'),
        ]

    @classmethod
    def random_quote(cls):
        """
        Возвращение случайной цитаты с учетом веса.
        """
        total_weight = sum(quote.weight for quote in cls.objects.all())
        random_value = random.randint(1, total_weight)
        cumulative_sum = 0
        for quote in cls.objects.all():
            cumulative_sum += quote.weight
            if cumulative_sum >= random_value:
                return quote
        return None