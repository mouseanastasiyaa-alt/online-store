from django import forms

from catalog.models import Product


# Список запрещённых слов для названий и описаний
FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей формы
        for field_name, field in self.fields.items():
            css_class = "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            field.widget.attrs["class"] = css_class

        # Плейсхолдеры для полей
        self.fields["name"].widget.attrs["placeholder"] = "Название товара"
        self.fields["description"].widget.attrs["placeholder"] = "Описание"
        self.fields["description"].widget.attrs["rows"] = 4
        self.fields["price"].widget.attrs["placeholder"] = "Цена"
        self.fields["price"].widget.attrs["step"] = "0.01"

    def _check_forbidden_words(self, value):
        """Проверяет, что в значении нет запрещённых слов (регистр игнорируется)."""
        if not value:
            return value
        lower_value = value.lower()
        for word in FORBIDDEN_WORDS:
            if word.lower() in lower_value:
                raise forms.ValidationError(
                    f"Слово «{word}» запрещено к использованию."
                )
        return value

    def clean_name(self):
        """Валидация названия на запрещённые слова."""
        return self._check_forbidden_words(self.cleaned_data.get("name"))

    def clean_description(self):
        """Валидация описания на запрещённые слова."""
        return self._check_forbidden_words(self.cleaned_data.get("description"))

    def clean_price(self):
        """Валидация цены: не может быть отрицательной."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and hasattr(image, "content_type"):
            if image.content_type not in ("image/jpeg", "image/png"):
                raise forms.ValidationError(
                    "Допустимые форматы изображения: JPEG или PNG."
                )
            max_size = 5 * 1024 * 1024  # 5 МБ
            if image.size > max_size:
                raise forms.ValidationError(
                    f"Размер изображения не должен превышать 5 МБ. "
                    f"Ваш файл: {image.size / 1024 / 1024:.2f} МБ."
                )
        return image