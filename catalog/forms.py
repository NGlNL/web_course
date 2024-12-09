from django import forms
from django.forms import BooleanField, ModelForm

from catalog.models import Product

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


class ContactForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Ваш e-mail", max_length=100)
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image",
            "category",
            "purchase_price",
            "unpublish",
        ]

    def clean_name(self):
        name = self.cleaned_data["name"].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(f"Недопустимое слово: {word}")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(f"Недопустимое слово: {word}")
        return description

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data["purchase_price"]
        if purchase_price < 0:
            raise forms.ValidationError("Цена продукта не может быть отрицательной")
        return purchase_price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла превышает 5 МБ")
            if image.content_type not in ["image/jpeg", "image/png"]:
                raise forms.ValidationError("Недопустимый формат файла")
        return image
