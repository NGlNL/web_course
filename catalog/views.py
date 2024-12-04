from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    FormView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import ContactForm, ProductForm
from .models import Product


class IndexListView(ListView):
    model = Product
    template_name = "catalog/index.html"
    context_object_name = "products"


class ContactView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение отправлено.")


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/products_details.html"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:index")
