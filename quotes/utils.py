import re
from uuid import uuid4
from pytils.translit import slugify

def unique_slugify(instance, slug):
    """Генератор уникальных SLUG для моделей, в случае существования такого SLUG."""
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug

def normalize_text(text):
    # Проверка, является ли текст строкой
    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split()).lower()
    return text