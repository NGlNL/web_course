from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Product


def index(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "catalog/index.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! Сообшение получено.")
    return render(request, "catalog/contacts.html")


def products_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/products_details.html", context)
